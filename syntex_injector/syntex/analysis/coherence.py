"""
SYNTX Coherence Analyzer - Cross-Field Kohärenz Bewertung
"""

import logging
from typing import Dict, List, Tuple, Optional

from .embeddings import semantic_similarity, get_embedding

logger = logging.getLogger("SYNTX.Coherence")

# Welche Felder sollten kohärent sein?
COHERENCE_PAIRS = {
    "SYNTEX_SYSTEM": [
        ("driftkorper", "kalibrierung", 0.3),   # min expected similarity
        ("kalibrierung", "stromung", 0.3),
        ("driftkorper", "stromung", 0.25),
    ],
    "HUMAN": [
        ("drift", "hintergrund_muster", 0.3),
        ("druckfaktoren", "wirkung", 0.3),
        ("tiefe", "klartext", 0.25),
    ],
    "SIGMA": [
        ("sigma_drift", "sigma_mechanismus", 0.3),
        ("sigma_strome", "sigma_frequenz", 0.25),
    ]
}

def analyze_pairwise_coherence(fields: Dict[str, str], format_type: str = "SYNTEX_SYSTEM") -> Dict:
    """Analysiert Kohärenz zwischen Feldpaaren"""
    pairs = COHERENCE_PAIRS.get(format_type, [])
    results = []
    total_score = 0.0
    valid_pairs = 0
    
    for field1, field2, min_expected in pairs:
        text1 = fields.get(field1, "")
        text2 = fields.get(field2, "")
        
        if text1 and text2:
            sim = semantic_similarity(text1, text2)
            passed = sim >= min_expected
            results.append({
                "pair": f"{field1} <-> {field2}",
                "similarity": round(sim, 3),
                "min_expected": min_expected,
                "passed": passed
            })
            total_score += sim
            valid_pairs += 1
    
    avg_coherence = total_score / valid_pairs if valid_pairs > 0 else 0.0
    
    return {
        "format": format_type,
        "pairs_analyzed": valid_pairs,
        "average_coherence": round(avg_coherence, 3),
        "details": results
    }

def calculate_coherence_score(fields: Dict[str, str], format_type: str = "SYNTEX_SYSTEM") -> float:
    """Berechnet einen einzelnen Kohärenz-Score (0.0 - 1.0)"""
    result = analyze_pairwise_coherence(fields, format_type)
    return result["average_coherence"]

def detect_incoherence(fields: Dict[str, str], format_type: str = "SYNTEX_SYSTEM") -> List[str]:
    """Findet inkohärente Feldpaare"""
    result = analyze_pairwise_coherence(fields, format_type)
    warnings = []
    for detail in result["details"]:
        if not detail["passed"]:
            warnings.append(f"Low coherence: {detail['pair']} = {detail['similarity']}")
    return warnings

if __name__ == "__main__":
    print("=== SYNTX COHERENCE TEST ===")
    
    # Test mit kohärenten Feldern
    coherent = {
        "driftkorper": "Die Struktur des Systems zeigt eine hierarchische Organisation mit klaren Ebenen.",
        "kalibrierung": "Das System passt sich durch Feedback-Mechanismen an veränderte Bedingungen an.",
        "stromung": "Informationsflüsse verbinden die verschiedenen Systemebenen miteinander."
    }
    
    # Test mit inkohärenten Feldern
    incoherent = {
        "driftkorper": "Pizza ist ein beliebtes italienisches Gericht mit Tomaten und Käse.",
        "kalibrierung": "Der Aktienmarkt reagiert auf politische Entscheidungen.",
        "stromung": "Elefanten leben in Afrika und Asien in großen Herden."
    }
    
    print("\nKohärente Felder:")
    r1 = analyze_pairwise_coherence(coherent)
    print(f"  Average: {r1['average_coherence']}")
    
    print("\nInkohärente Felder:")
    r2 = analyze_pairwise_coherence(incoherent)
    print(f"  Average: {r2['average_coherence']}")
    
    print("\n✅ Coherence OK" if r1['average_coherence'] > r2['average_coherence'] else "❌ Test failed")
