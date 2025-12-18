"""
SYNTX Quality Scoring System

=== ZWECK ===
Bewertet SYNTX Response Quality für ALLE Formate:
1. SIGMA Protocol (6 Felder)
2. Human-Readable (6 Felder)
3. SYNTEX_SYSTEM (3 Felder)

=== DESIGN ===
Format-Aware Scoring
Jedes Format hat eigene Completeness-Logik
SYNTEX_SYSTEM: 3/3 Felder = 100%
Human/SIGMA: 6/6 Felder = 100%

=== FLOW ===
1. Detect Format (via fields.get_format())
2. Apply entsprechende Weights
3. Calculate Completeness
4. Return QualityScore
"""

from typing import Dict
from dataclasses import dataclass

from ..core.parser import SyntexFields


@dataclass
class QualityScore:
    """
    SYNTX Quality Metrics
    
    === FIELDS ===
    - total_score: Gesamt (0-100)
    - field_completeness: Felder vollständig? (0-100)
    - structure_adherence: Struktur korrekt? (0-100)
    - detail_breakdown: Dict mit Feld → Bool
    """
    total_score: int
    field_completeness: int
    structure_adherence: int
    detail_breakdown: Dict[str, bool]
    
    def to_dict(self) -> Dict:
        return {
            "total_score": self.total_score,
            "field_completeness": self.field_completeness,
            "structure_adherence": self.structure_adherence,
            "detail_breakdown": self.detail_breakdown
        }


class SyntexScorer:
    """
    SYNTX Quality Scorer
    
    === TERMINOLOGIEN ===
    Unterstützt alle 3 Formate mit eigenen Weights
    
    === WEIGHTS ===
    Human/SIGMA: 6 Felder, je nach Wichtigkeit gewichtet
    SYNTEX_SYSTEM: 3 Felder, gleichmäßig verteilt
    """
    
    def __init__(self):
        # === HUMAN-READABLE WEIGHTS ===
        self.human_field_weights = {
            "drift": 15,
            "hintergrund_muster": 20,
            "druckfaktoren": 15,
            "tiefe": 20,
            "wirkung": 20,
            "klartext": 10
        }
        
        # === SIGMA PROTOCOL WEIGHTS ===
        self.sigma_field_weights = {
            "sigma_drift": 15,
            "sigma_mechanismus": 20,
            "sigma_frequenz": 15,
            "sigma_dichte": 20,
            "sigma_strome": 20,
            "sigma_extrakt": 10
        }
        
        # === SYNTEX_SYSTEM WEIGHTS ===
        # 3 Felder, gleichmäßig verteilt = 33.33% each
        self.syntex_system_weights = {
            "driftkorper": 33,
            "kalibrierung": 34,
            "stromung": 33
        }
    
    def score(self, fields: SyntexFields, response_text: str) -> QualityScore:
        """
        Bewertet SYNTX Quality - Format-Aware
        
        Args:
            fields: Parsed SyntexFields
            response_text: Original Response (für Structure Check)
        
        Returns:
            QualityScore mit allen Metriken
        """
        
        field_scores = {}
        total_field_score = 0
        
        # === FORMAT DETECTION ===
        format_type = fields.get_format()
        
        if format_type == "SIGMA":
            # SIGMA Scoring
            weights = self.sigma_field_weights
            field_list = ["sigma_drift", "sigma_mechanismus", "sigma_frequenz", 
                         "sigma_dichte", "sigma_strome", "sigma_extrakt"]
            structure_markers = ["1.", "2.", "3.", "4.", "5.", "6."]
        
        elif format_type == "SYNTEX_SYSTEM":
            # SYNTEX_SYSTEM Scoring
            weights = self.syntex_system_weights
            field_list = ["driftkorper", "kalibrierung", "stromung"]
            structure_markers = ["###"]  # Markdown headers
        
        else:
            # Human-Readable Scoring
            weights = self.human_field_weights
            field_list = ["drift", "hintergrund_muster", "druckfaktoren", 
                         "tiefe", "wirkung", "klartext"]
            structure_markers = ["1.", "2.", "3.", "4.", "5.", "6."]
        
        # === FIELD COMPLETENESS ===
        for field_name in field_list:
            weight = weights.get(field_name, 0)
            field_value = getattr(fields, field_name)
            has_content = field_value is not None and len(field_value.strip()) > 0
            field_scores[field_name] = has_content
            
            if has_content:
                total_field_score += weight
        
        field_completeness = total_field_score
        
        # === STRUCTURE ADHERENCE ===
        structure_score = 0
        for marker in structure_markers:
            if marker in response_text:
                structure_score += 100 // len(structure_markers)
        
        # Cap at 100
        structure_score = min(structure_score, 100)
        
        # === TOTAL SCORE ===
        # 70% Completeness, 30% Structure
        total_score = int((field_completeness * 0.7) + (structure_score * 0.3))
        
        return QualityScore(
            total_score=total_score,
            field_completeness=field_completeness,
            structure_adherence=structure_score,
            detail_breakdown=field_scores
        )
    
    def format_score_output(self, score: QualityScore) -> str:
        """
        Formatiert Score für Terminal-Ausgabe
        
        Args:
            score: QualityScore Objekt
        
        Returns:
            Formatierter String für Terminal
        """
        output = []
        output.append(f"\n📊 SYNTEX Quality Score: {score.total_score}/100")
        output.append(f"   Field Completeness: {score.field_completeness}/100")
        output.append(f"   Structure Adherence: {score.structure_adherence}/100")
        output.append("\nField Breakdown:")
        
        for field, present in score.detail_breakdown.items():
            icon = "✅" if present else "❌"
            field_display = field.upper().replace('_', ' ')
            output.append(f"   {icon} {field_display}")
        
        return "\n".join(output)
