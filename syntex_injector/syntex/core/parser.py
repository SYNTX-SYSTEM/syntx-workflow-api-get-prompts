"""
SYNTX Response Parser - Alle Terminologien

=== ZWECK ===
Erkennt und parsed ALLE SYNTX Formate:
1. SIGMA Protocol (Σ-Notation)
2. Human-Readable (DRIFT, HINTERGRUND-MUSTER, etc.)
3. SYNTEX_SYSTEM (Driftkörperanalyse, Strömungsverhältnisse, etc.)

=== DESIGN ===
Felddenken statt Objektdenken
Parser erkennt Resonanzmuster in Response
Nicht Token-Ebene → Feld-Ebene

=== FLOW ===
1. Detect Format (SIGMA vs Human vs SYNTEX_SYSTEM)
2. Extract Fields via Regex
3. Return SyntexFields mit allen detected Feldern
"""

import re
from typing import Dict, Optional, List
from dataclasses import dataclass, field

from ..utils.exceptions import ParseError, FieldMissingError


@dataclass
class SyntexFields:
    """
    SYNTX Felder Container - Alle Terminologien
    
    === FELDER ===
    SIGMA Protocol:
      - sigma_drift, sigma_mechanismus, sigma_frequenz
      - sigma_dichte, sigma_strome, sigma_extrakt
    
    Human-Readable:
      - drift, hintergrund_muster, druckfaktoren
      - tiefe, wirkung, klartext
    
    SYNTEX_SYSTEM:
      - driftkorper, kalibrierung, stromung
    
    === KOHÄRENZ ===
    Nur EIN Format pro Response wird befüllt
    Entweder SIGMA oder Human oder SYNTEX_SYSTEM
    Niemals gemischt (außer bei Drift)
    """
    
    # === SIGMA PROTOCOL ===
    sigma_drift: Optional[str] = None
    sigma_mechanismus: Optional[str] = None
    sigma_frequenz: Optional[str] = None
    sigma_dichte: Optional[str] = None
    sigma_strome: Optional[str] = None
    sigma_extrakt: Optional[str] = None
    
    # === HUMAN-READABLE ===
    drift: Optional[str] = None
    hintergrund_muster: Optional[str] = None
    druckfaktoren: Optional[str] = None
    tiefe: Optional[str] = None
    wirkung: Optional[str] = None
    klartext: Optional[str] = None
    
    # === SYNTEX_SYSTEM ===
    driftkorper: Optional[str] = None
    kalibrierung: Optional[str] = None
    stromung: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Alle Felder als Dict"""
        return {
            # SIGMA
            "sigma_drift": self.sigma_drift,
            "sigma_mechanismus": self.sigma_mechanismus,
            "sigma_frequenz": self.sigma_frequenz,
            "sigma_dichte": self.sigma_dichte,
            "sigma_strome": self.sigma_strome,
            "sigma_extrakt": self.sigma_extrakt,
            
            # Human
            "drift": self.drift,
            "hintergrund_muster": self.hintergrund_muster,
            "druckfaktoren": self.druckfaktoren,
            "tiefe": self.tiefe,
            "wirkung": self.wirkung,
            "klartext": self.klartext,
            
            # SYNTEX_SYSTEM
            "driftkorper": self.driftkorper,
            "kalibrierung": self.kalibrierung,
            "stromung": self.stromung,
        }
    
    def missing_fields(self) -> List[str]:
        """
        Welche Felder fehlen im detected Format?
        
        Returns:
            Liste der fehlenden Feldnamen
        """
        missing = []
        
        if self.is_sigma():
            # SIGMA Format - 6 Felder required
            sigma_fields = {
                "sigma_drift": self.sigma_drift,
                "sigma_mechanismus": self.sigma_mechanismus,
                "sigma_frequenz": self.sigma_frequenz,
                "sigma_dichte": self.sigma_dichte,
                "sigma_strome": self.sigma_strome,
                "sigma_extrakt": self.sigma_extrakt
            }
            for field_name, value in sigma_fields.items():
                if value is None or value.strip() == "":
                    missing.append(field_name)
        
        elif self.is_syntex_system():
            # SYNTEX_SYSTEM Format - 3 Felder required
            system_fields = {
                "driftkorper": self.driftkorper,
                "kalibrierung": self.kalibrierung,
                "stromung": self.stromung,
            }
            for field_name, value in system_fields.items():
                if value is None or value.strip() == "":
                    missing.append(field_name)
        
        else:
            # Human Format - 6 Felder required
            human_fields = {
                "drift": self.drift,
                "hintergrund_muster": self.hintergrund_muster,
                "druckfaktoren": self.druckfaktoren,
                "tiefe": self.tiefe,
                "wirkung": self.wirkung,
                "klartext": self.klartext
            }
            for field_name, value in human_fields.items():
                if value is None or value.strip() == "":
                    missing.append(field_name)
        
        return missing
    
    def is_complete(self) -> bool:
        """Alle Felder des detected Formats vorhanden?"""
        return len(self.missing_fields()) == 0
    
    def is_sigma(self) -> bool:
        """Ist SIGMA Protocol Format?"""
        return any([
            self.sigma_drift,
            self.sigma_mechanismus,
            self.sigma_frequenz,
            self.sigma_dichte,
            self.sigma_strome,
            self.sigma_extrakt
        ])
    
    def is_syntex_system(self) -> bool:
        """Ist SYNTEX_SYSTEM Format?"""
        return any([
            self.driftkorper,
            self.kalibrierung,
            self.stromung,
        ])
    
    def get_format(self) -> str:
        """Welches Format wurde detected?"""
        if self.is_sigma():
            return "SIGMA"
        elif self.is_syntex_system():
            return "SYNTEX_SYSTEM"
        else:
            return "HUMAN"


class SyntexParser:
    """
    SYNTX Response Parser
    
    === STRATEGIE ===
    1. Detect Format via Marker-Strings
    2. Apply entsprechende Regex Patterns
    3. Extract Felder
    4. Return SyntexFields
    
    === ROBUSTHEIT ===
    - Case-insensitive matching
    - Whitespace-tolerant
    - Greedy field extraction
    """
    
    def __init__(self):
        pass
    
    def parse(self, response: str) -> SyntexFields:
        """
        Parse SYNTX Response in beliebigem Format
        
        Args:
            response: Raw Model Output
        
        Returns:
            SyntexFields mit extracted Feldern
        
        Raises:
            ParseError wenn Response leer
        """
        if not response or response.strip() == "":
            raise ParseError("Empty response")
        
        fields = SyntexFields()
        
        # === FORMAT DETECTION & EXTRACTION ===
        
        # 1. SIGMA PROTOCOL
        if "Σ-DRIFTGRADIENT" in response or "Σ-MECHANISMUSKNOTEN" in response:
            self._parse_sigma(response, fields)
        
        # 2. SYNTEX_SYSTEM FORMAT
        elif "Driftkörperanalyse" in response or "Strömungsverhältnisse" in response or "Kalibrierung" in response:
            self._parse_syntex_system(response, fields)
        
        # 3. HUMAN-READABLE FORMAT
        else:
            self._parse_human(response, fields)
        
        return fields
    
    def _parse_sigma(self, response: str, fields: SyntexFields) -> None:
        """
        Parse SIGMA Protocol Format
        
        Pattern: 1. Σ-DRIFTGRADIENT ... 2. Σ-MECHANISMUSKNOTEN ...
        """
        patterns = [
            (r"1\.\s*Σ-DRIFTGRADIENT.*?(?=2\.|$)", "sigma_drift"),
            (r"2\.\s*Σ-MECHANISMUSKNOTEN.*?(?=3\.|$)", "sigma_mechanismus"),
            (r"3\.\s*Σ-FREQUENZFELD.*?(?=4\.|$)", "sigma_frequenz"),
            (r"4\.\s*Σ-DICHTELEVEL.*?(?=5\.|$)", "sigma_dichte"),
            (r"5\.\s*Σ-ZWEISTRÖME.*?(?=6\.|$)", "sigma_strome"),
            (r"6\.\s*Σ-KERNEXTRAKT.*?$", "sigma_extrakt")
        ]
        
        for pattern, field_name in patterns:
            match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
            if match:
                content = match.group(0).strip()
                # Remove field header (1. Σ-DRIFTGRADIENT:)
                content = re.sub(r"^\d+\.\s*Σ-[A-Z]+\s*[-:]?\s*", "", content, flags=re.IGNORECASE)
                setattr(fields, field_name, content.strip())
    
    def _parse_syntex_system(self, response: str, fields: SyntexFields) -> None:
        """
        Parse SYNTEX_SYSTEM Format
        
        Pattern: ### Driftkörperanalyse: ... ### Kalibrierung: ...
        """
        patterns = [
            (r"###\s*Driftkörperanalyse[:\s]*(.*?)(?=###|$)", "driftkorper"),
            (r"###\s*Kalibrierung[:\s]*(.*?)(?=###|$)", "kalibrierung"),
            (r"###\s*Strömungsverhältnisse[:\s]*(.*?)(?=###|$)", "stromung"),
        ]
        
        for pattern, field_name in patterns:
            match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
            if match:
                content = match.group(1).strip()
                setattr(fields, field_name, content)
    
    def _parse_human(self, response: str, fields: SyntexFields) -> None:
        """
        Parse Human-Readable Format
        
        Pattern: 1. DRIFT: ... 2. HINTERGRUND-MUSTER: ...
        """
        patterns = [
            (r"1\.\s*DRIFT[:\s]*(.*?)(?=\n\s*2\.|$)", "drift"),
            (r"2\.\s*HINTERGRUND[-\s]*MUSTER[:\s]*(.*?)(?=\n\s*3\.|$)", "hintergrund_muster"),
            (r"3\.\s*DRUCKFAKTOREN[:\s]*(.*?)(?=\n\s*4\.|$)", "druckfaktoren"),
            (r"4\.\s*TIEFE[:\s]*(.*?)(?=\n\s*5\.|$)", "tiefe"),
            (r"5\.\s*WIRKUNG.*?(?=\n\s*6\.|$)", "wirkung"),
            (r"6\.\s*KLARTEXT[:\s]*(.*?)$", "klartext")
        ]
        
        for pattern, field_name in patterns:
            match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
            if match:
                if match.lastindex:
                    # Group 1 exists - use it
                    setattr(fields, field_name, match.group(1).strip())
                else:
                    # No groups - use full match and clean
                    content = match.group(0).strip()
                    content = re.sub(r"^\d+\.\s*[A-Z\s-]+[:\s]*", "", content, flags=re.IGNORECASE)
                    setattr(fields, field_name, content.strip())
    
    def validate(self, fields: SyntexFields, strict: bool = False) -> bool:
        """
        Validiere ob alle Felder vorhanden
        
        Args:
            fields: Zu validierende Felder
            strict: Wenn True, raise Exception bei fehlenden Feldern
        
        Returns:
            True wenn komplett, False sonst
        
        Raises:
            FieldMissingError wenn strict=True und Felder fehlen
        """
        missing = fields.missing_fields()
        if missing and strict:
            raise FieldMissingError(missing)
        return len(missing) == 0
