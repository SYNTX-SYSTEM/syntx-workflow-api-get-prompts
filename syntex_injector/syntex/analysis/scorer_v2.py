"""
SYNTX Semantic Scorer v2.0 - Vollständige semantische Bewertung

=== SCORE KOMPONENTEN ===
1. Field Presence (20%)  - Feld existiert und nicht leer
2. Semantic Similarity (35%) - Inhalt passt zur Feld-Definition
3. Cross-Coherence (25%) - Felder sind untereinander kohärent
4. Content Depth (15%) - Länge, Keywords, Komplexität
5. Structure (5%) - Markdown, Format korrekt

=== STATUS LEVELS ===
- FAILED:    < 40%
- UNSTABLE:  40-59%
- OK:        60-84%
- EXCELLENT: >= 85%
"""

import logging
from typing import Dict, List, Optional
from dataclasses import dataclass, field

from .field_definitions import (
    get_field_definition, get_all_field_names, 
    SYNTEX_SYSTEM_FIELDS, HUMAN_READABLE_FIELDS, SIGMA_FIELDS
)
from .embeddings import semantic_similarity, keyword_coverage
from .coherence import calculate_coherence_score

logger = logging.getLogger("SYNTX.ScorerV2")

# Score Weights
WEIGHTS = {
    "presence": 0.20,
    "similarity": 0.35,
    "coherence": 0.25,
    "depth": 0.15,
    "structure": 0.05
}

@dataclass
class FieldScore:
    """Score für ein einzelnes Feld"""
    field_name: str
    presence_score: float = 0.0
    similarity_score: float = 0.0
    coherence_score: float = 0.0
    depth_score: float = 0.0
    structure_score: float = 0.0
    total_score: float = 0.0
    status: str = "FAILED"
    warnings: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "field": self.field_name,
            "presence_score": round(self.presence_score, 3),
            "similarity_score": round(self.similarity_score, 3),
            "coherence_score": round(self.coherence_score, 3),
            "depth_score": round(self.depth_score, 3),
            "structure_score": round(self.structure_score, 3),
            "total_score": round(self.total_score, 3),
            "status": self.status,
            "warnings": self.warnings
        }

@dataclass 
class QualityScoreV2:
    """Gesamtscore für alle Felder"""
    total_score: float = 0.0
    total_score_100: int = 0
    status: str = "FAILED"
    format_type: str = "SYNTEX_SYSTEM"
    field_scores: Dict[str, FieldScore] = field(default_factory=dict)
    coherence_score: float = 0.0
    warnings: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "total_score": round(self.total_score, 3),
            "total_score_100": self.total_score_100,
            "status": self.status,
            "format": self.format_type,
            "coherence": round(self.coherence_score, 3),
            "fields": {k: v.to_dict() for k, v in self.field_scores.items()},
            "warnings": self.warnings
        }

def _get_status(score: float) -> str:
    """Bestimmt Status basierend auf Score"""
    if score >= 0.85:
        return "EXCELLENT"
    elif score >= 0.60:
        return "OK"
    elif score >= 0.40:
        return "UNSTABLE"
    return "FAILED"

def _score_presence(text: str) -> float:
    """Bewertet ob Feld existiert und nicht leer"""
    if not text or not text.strip():
        return 0.0
    return 1.0

def _score_depth(text: str, field_def: Dict) -> float:
    """Bewertet Content-Tiefe: Länge und Keywords"""
    if not text:
        return 0.0
    
    text = text.strip()
    min_len = field_def.get("min_length", 50)
    ideal_len = field_def.get("ideal_length", 200)
    keywords = field_def.get("keywords", [])
    
    # Längen-Score (0-0.5)
    text_len = len(text)
    if text_len >= ideal_len:
        len_score = 0.5
    elif text_len >= min_len:
        len_score = 0.3 + 0.2 * (text_len - min_len) / (ideal_len - min_len)
    elif text_len > 0:
        len_score = 0.3 * (text_len / min_len)
    else:
        len_score = 0.0
    
    # Keyword-Score (0-0.5)
    kw_score = keyword_coverage(text, keywords) * 0.5 if keywords else 0.25
    
    return min(1.0, len_score + kw_score)

def _score_structure(text: str) -> float:
    """Bewertet Struktur: Markdown, Absätze, etc."""
    if not text:
        return 0.0
    
    score = 0.5  # Basis
    
    # Bonus für Struktur-Elemente
    if "###" in text or "**" in text:
        score += 0.2
    if "\n\n" in text or len(text.split("\n")) > 2:
        score += 0.15
    if ":" in text or "-" in text:
        score += 0.15
    
    return min(1.0, score)

def _score_similarity(text: str, field_def: Dict) -> float:
    """Bewertet semantische Ähnlichkeit zur Feld-Definition"""
    if not text:
        return 0.0
    
    description = field_def.get("description", "")
    ideal = field_def.get("ideal_response", "")
    
    if not description and not ideal:
        return 0.5  # Neutral wenn keine Definition
    
    # Similarity zu Description und Ideal Response
    scores = []
    if description:
        scores.append(semantic_similarity(text, description))
    if ideal:
        scores.append(semantic_similarity(text, ideal))
    
    return sum(scores) / len(scores) if scores else 0.5

def score_field(field_name: str, field_value: str, all_fields: Dict[str, str], 
                format_type: str = "SYNTEX_SYSTEM") -> FieldScore:
    """Bewertet ein einzelnes Feld semantisch"""
    
    result = FieldScore(field_name=field_name)
    field_def = get_field_definition(field_name)
    
    if not field_def:
        result.warnings.append(f"No definition for field: {field_name}")
        return result
    
    # 1. Presence (20%)
    result.presence_score = _score_presence(field_value)
    
    # 2. Similarity (35%)
    result.similarity_score = _score_similarity(field_value, field_def)
    
    # 3. Coherence (25%) - wird später auf Gesamtebene berechnet
    result.coherence_score = 0.0  # Placeholder
    
    # 4. Depth (15%)
    result.depth_score = _score_depth(field_value, field_def)
    
    # 5. Structure (5%)
    result.structure_score = _score_structure(field_value)
    
    # Warnings
    if result.presence_score == 0:
        result.warnings.append("Field is empty")
    if result.similarity_score < 0.3:
        result.warnings.append("Low semantic match to field definition")
    if result.depth_score < 0.3:
        result.warnings.append("Content lacks depth")
    
    # Total (ohne Coherence - wird später addiert)
    result.total_score = (
        result.presence_score * WEIGHTS["presence"] +
        result.similarity_score * WEIGHTS["similarity"] +
        result.depth_score * WEIGHTS["depth"] +
        result.structure_score * WEIGHTS["structure"]
    )
    
    result.status = _get_status(result.total_score)
    return result

def score_all_fields(fields: Dict[str, str], format_type: str = "SYNTEX_SYSTEM") -> QualityScoreV2:
    """Bewertet alle Felder und berechnet Gesamtscore"""
    
    result = QualityScoreV2(format_type=format_type)
    expected_fields = get_all_field_names(format_type)
    
    if not expected_fields:
        result.warnings.append(f"Unknown format: {format_type}")
        return result
    
    # Score jedes Feld
    for field_name in expected_fields:
        field_value = fields.get(field_name, "")
        field_score = score_field(field_name, field_value, fields, format_type)
        result.field_scores[field_name] = field_score
    
    # Coherence Score (global)
    result.coherence_score = calculate_coherence_score(fields, format_type)
    
    # Update Coherence in allen Field Scores
    for fs in result.field_scores.values():
        fs.coherence_score = result.coherence_score
        # Recalculate total with coherence
        fs.total_score = (
            fs.presence_score * WEIGHTS["presence"] +
            fs.similarity_score * WEIGHTS["similarity"] +
            fs.coherence_score * WEIGHTS["coherence"] +
            fs.depth_score * WEIGHTS["depth"] +
            fs.structure_score * WEIGHTS["structure"]
        )
        fs.status = _get_status(fs.total_score)
    
    # Gesamtscore = Durchschnitt aller Felder
    if result.field_scores:
        result.total_score = sum(fs.total_score for fs in result.field_scores.values()) / len(result.field_scores)
    
    result.total_score_100 = int(result.total_score * 100)
    result.status = _get_status(result.total_score)
    
    # Global Warnings
    if result.coherence_score < 0.3:
        result.warnings.append("Low cross-field coherence")
    if result.total_score < 0.4:
        result.warnings.append("Overall quality below threshold")
    
    return result

# Kompatibilität mit altem Scorer
def score_response(fields, format_type: str = "SYNTEX_SYSTEM") -> QualityScoreV2:
    """Alias für score_all_fields - Kompatibilität"""
    if hasattr(fields, 'to_dict'):
        fields_dict = {k: v for k, v in fields.to_dict().items() if v}
    else:
        fields_dict = fields
    return score_all_fields(fields_dict, format_type)

if __name__ == "__main__":
    print("=== SYNTX SCORER V2.0 TEST ===\n")
    
    # Test mit guten SYNTX Feldern
    good_fields = {
        "driftkorper": """
        ### Driftkörperanalyse:
        Die Struktur zeigt eine hierarchische Organisation auf vier Ebenen.
        TIER-1: Sichtbare Oberfläche mit klaren Komponenten.
        TIER-2: Innere Verbindungen und Modulstruktur.
        TIER-3: Mechanismen der Selbstregulation.
        TIER-4: Der Kern ist ein adaptives Netzwerk.
        """,
        "kalibrierung": """
        ### Kalibrierungsverhältnisse:
        Das System passt sich durch Feedback-Mechanismen an.
        Dynamische Justierung bei Störungen.
        Selbstregulation über mehrere Ebenen.
        Anpassung ist das zentrale Prinzip.
        """,
        "stromung": """
        ### Strömungsverhältnisse:
        Informationsflüsse verbinden alle Ebenen.
        Daten zirkulieren von Oberfläche zum Kern.
        Energie fließt durch hierarchische Strukturen.
        Der Kreislauf erhält Gleichgewicht.
        """
    }
    
    print("Testing GOOD fields...")
    result = score_all_fields(good_fields, "SYNTEX_SYSTEM")
    print(f"Total Score: {result.total_score_100}/100")
    print(f"Status: {result.status}")
    print(f"Coherence: {result.coherence_score:.3f}")
    
    for name, fs in result.field_scores.items():
        print(f"\n  {name}:")
        print(f"    Presence:   {fs.presence_score:.2f}")
        print(f"    Similarity: {fs.similarity_score:.2f}")
        print(f"    Depth:      {fs.depth_score:.2f}")
        print(f"    Structure:  {fs.structure_score:.2f}")
        print(f"    Total:      {fs.total_score:.2f} ({fs.status})")
    
    print("\n" + "="*50)
    print("\nTesting BAD fields...")
    
    bad_fields = {
        "driftkorper": "Pizza",
        "kalibrierung": "Aktien",
        "stromung": ""
    }
    
    result2 = score_all_fields(bad_fields, "SYNTEX_SYSTEM")
    print(f"Total Score: {result2.total_score_100}/100")
    print(f"Status: {result2.status}")
    print(f"Warnings: {result2.warnings}")
    
    print("\n" + "="*50)
    if result.total_score > result2.total_score:
        print("✅ SCORER V2.0 WORKING - Good > Bad")
    else:
        print("❌ SCORER V2.0 FAILED")
