"""
File Handler - Atomic File Operations für Queue

=== ZWECK ===
Sichere, atomare Datei-Operationen für Queue-System
Verhindert Race Conditions und Partial Writes

=== ATOMIC OPERATIONS ===
1. Write: tmp → rename (atomic auf POSIX)
2. Move: rename (atomic auf POSIX)
3. Delete: unlink (atomic)

=== GARANTIEN ===
- Keine partial writes
- Keine race conditions
- Keine lost updates
- Filesystem als Single Source of Truth
"""
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Config importieren
from ..config.queue_config import *


class FileHandler:
    """
    Atomic File Operations für Queue
    
    === DESIGN PATTERN ===
    Command Pattern - jede Operation ist atomic und kann nicht halb-fertig sein
    
    === THREAD-SAFETY ===
    Atomic durch POSIX rename() syscall
    Mehrere Handler können parallel laufen ohne Konflikte
    """
    
    def atomic_write(
        self, 
        content: str, 
        metadata: Dict[str, Any], 
        target_dir: Path
    ) -> Path:
        """
        Schreibt Datei ATOMIC in Queue
        
        === PATTERN ===
        1. Schreibe in .tmp/ (niemand sieht es)
        2. rename zu target_dir/ (atomic, instant visible)
        
        === WARUM ATOMIC ===
        Wenn Prozess crashed während Write:
        - Partial File bleibt in .tmp/
        - Nichts landet in incoming/
        - Kein Consumer sieht broken File
        
        === FILENAME PATTERN ===
        YYYYMMDD_HHMMSS_ffffff__topic_XXX__style_YYY.txt
        
        Sortierung:
        - Nach Timestamp (älteste zuerst)
        - Metadata im Filename (grep-bar)
        
        === ARGS ===
        content: Meta-Prompt Text
        metadata: Dict mit topic, style, category, gpt_quality, gpt_cost
        target_dir: Ziel-Ordner (meist queue/incoming)
        
        === RETURNS ===
        Path: Finaler Pfad der geschriebenen Datei
        """
        # Timestamp mit Microsekunden für Eindeutigkeit
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        
        # Topic für Filename (max 30 chars, slug)
        topic_slug = self._slugify(metadata.get('topic', 'unknown'))[:30]
        
        # Style für Filename
        style = metadata.get('style', 'unknown')
        
        # Filename bauen
        # Format: 20251128_092720_123456__topic_KI__style_technisch.txt
        filename = f"{timestamp}__topic_{topic_slug}__style_{style}.txt"
        
        # === PHASE 1: Write to temp ===
        # Temp-Pfad (.tmp ist hidden für Queue-System)
        temp_path = QUEUE_TMP / filename
        temp_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Content schreiben (kann Zeit dauern)
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Metadata schreiben (separate JSON)
        meta_path = temp_path.with_suffix('.json')
        with open(meta_path, 'w', encoding='utf-8') as f:
            # Timestamp hinzufügen
            metadata['created_at'] = datetime.now().isoformat()
            metadata['filename'] = filename
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        # === PHASE 2: Atomic Move ===
        # Ziel-Pfade
        final_path = target_dir / filename
        final_meta = final_path.with_suffix('.json')
        
        # Atomic rename (instant visible, no partial state)
        # Wenn das crashed: File bleibt in .tmp, nicht in incoming
        temp_path.rename(final_path)
        meta_path.rename(final_meta)
        
        return final_path
    
    def move_to_processed(self, job_path: Path) -> Path:
        """
        Verschiebt Job nach processed/
        
        === WANN ===
        Nach erfolgreicher SYNTX Kalibrierung
        
        === WAS PASSIERT ===
        1. Update Metadata (processed_at, status)
        2. Atomic Move: processing/ → processed/
        
        === ARGS ===
        job_path: Aktueller Pfad in processing/
        
        === RETURNS ===
        Path: Neuer Pfad in processed/
        """
        # Target bauen
        target = QUEUE_PROCESSED / job_path.name
        target_meta = target.with_suffix('.json')
        
        # Metadata updaten
        meta_path = job_path.with_suffix('.json')
        if meta_path.exists():
            with open(meta_path, 'r') as f:
                metadata = json.load(f)
            
            # Success Info hinzufügen
            metadata['processed_at'] = datetime.now().isoformat()
            metadata['status'] = 'success'
            
            # Zurückschreiben
            with open(meta_path, 'w') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        # Atomic Move
        job_path.rename(target)
        if meta_path.exists():
            meta_path.rename(target_meta)
        
        return target
    
    def move_to_error(
        self, 
        job_path: Path, 
        error_info: Dict[str, Any]
    ) -> Path:
        """
        Verschiebt Job nach error/ mit Retry-Count
        
        === WANN ===
        Nach fehlgeschlagener Kalibrierung
        
        === RETRY PATTERN ===
        - job.txt → job__retry1.txt (1. Fehler)
        - job__retry1.txt → job__retry2.txt (2. Fehler)
        - job__retry2.txt → job__retry3.txt (3. Fehler, dann stop)
        
        === METADATA ===
        - retry_count: Anzahl Versuche
        - last_error: Error Info vom letzten Versuch
        - failed_at: Timestamp
        
        === ARGS ===
        job_path: Aktueller Pfad in processing/
        error_info: Dict mit error details
        
        === RETURNS ===
        Path: Neuer Pfad in error/
        """
        # Metadata laden
        meta_path = job_path.with_suffix('.json')
        if meta_path.exists():
            with open(meta_path, 'r') as f:
                metadata = json.load(f)
        else:
            metadata = {}
        
        # Retry Count erhöhen
        retry_count = metadata.get('retry_count', 0) + 1
        metadata['retry_count'] = retry_count
        metadata['last_error'] = error_info
        metadata['failed_at'] = datetime.now().isoformat()
        metadata['status'] = 'error'
        
        # Neuer Filename mit Retry-Count
        base = job_path.stem  # Ohne Extension
        new_filename = f"{base}__retry{retry_count}.txt"
        
        # Target bauen
        target = QUEUE_ERROR / new_filename
        target_meta = target.with_suffix('.json')
        
        # Metadata schreiben
        with open(meta_path, 'w') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        # Atomic Move
        job_path.rename(target)
        meta_path.rename(target_meta)
        
        return target
    
    def _slugify(self, text: str) -> str:
        """
        Macht String filename-safe
        
        === TRANSFORMATIONEN ===
        - Lowercase
        - Spaces → Underscores
        - Nur [a-z0-9_-]
        
        === BEISPIEL ===
        "Künstliche Intelligenz!" → "kunstliche_intelligenz"
        """
        # Lowercase
        text = text.lower()
        
        # Umlaute ersetzen
        replacements = {
            'ä': 'ae', 'ö': 'oe', 'ü': 'ue',
            'ß': 'ss', ' ': '_', '-': '_'
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # Nur erlaubte Zeichen
        allowed = 'abcdefghijklmnopqrstuvwxyz0123456789_'
        text = ''.join(c for c in text if c in allowed)
        
        return text


# === MAIN BLOCK ===
if __name__ == "__main__":
    # Quick Test
    handler = FileHandler()
    
    # Test Content
    test_content = "Dies ist ein Test Meta-Prompt über KI."
    test_metadata = {
        "topic": "Künstliche Intelligenz",
        "style": "technisch",
        "category": "technologie",
        "gpt_quality": {"total_score": 8},
        "gpt_cost": {"total_cost": 0.002}
    }
    
    # Write Test
    print("Writing test file...")
    result = handler.atomic_write(
        content=test_content,
        metadata=test_metadata,
        target_dir=QUEUE_INCOMING
    )
    
    print(f"✅ Written: {result}")
    print(f"✅ Check: ls queue/incoming/")
