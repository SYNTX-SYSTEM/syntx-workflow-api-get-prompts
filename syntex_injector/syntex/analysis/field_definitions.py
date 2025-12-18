"""
SYNTX Field Definitions - Semantische Referenzen für Scoring v2.0
"""

from typing import Dict, List, Optional

SYNTEX_SYSTEM_FIELDS: Dict[str, Dict] = {
    "driftkorper": {
        "description": "Der Driftkörper beschreibt WAS das analysierte Objekt IST auf vier TIER-Ebenen.",
        "ideal_response": "Vollständige Analyse von Oberfläche bis Kern mit allen vier TIERs.",
        "keywords": ["erscheinung", "struktur", "mechanismus", "kern", "wesen", "tier-1", "tier-2", "tier-3", "tier-4"],
        "anti_keywords": ["vielleicht", "unklar", "keine ahnung"],
        "min_length": 150,
        "ideal_length": 400,
        "weight": 33,
        "requires_tiers": True
    },
    "kalibrierung": {
        "description": "Die Kalibrierung beschreibt wie sich das System VERÄNDERT und ANPASST.",
        "ideal_response": "Analyse von Anpassungsmechanismen, Feedback-Loops und Selbstregulation.",
        "keywords": ["anpassung", "veränderung", "feedback", "transformation", "dynamik", "regulation"],
        "anti_keywords": ["statisch", "unveränderlich", "starr"],
        "min_length": 100,
        "ideal_length": 300,
        "weight": 34,
        "requires_tiers": False
    },
    "stromung": {
        "description": "Die Strömung beschreibt wie Energie, Information und Materie FLIESSEN.",
        "ideal_response": "Analyse von Energieflüssen, Informationsströmen und Kreisläufen.",
        "keywords": ["fluss", "strom", "energie", "information", "transfer", "kreislauf"],
        "anti_keywords": ["blockiert", "gestoppt", "stagnation"],
        "min_length": 100,
        "ideal_length": 300,
        "weight": 33,
        "requires_tiers": False
    }
}

HUMAN_READABLE_FIELDS: Dict[str, Dict] = {
    "drift": {"description": "Bewegungsrichtung und Tendenz", "keywords": ["richtung", "tendenz", "bewegung"], "min_length": 50, "ideal_length": 150, "weight": 15},
    "hintergrund_muster": {"description": "Verborgene Strukturen und Muster", "keywords": ["muster", "struktur", "schema"], "min_length": 80, "ideal_length": 200, "weight": 20},
    "druckfaktoren": {"description": "Kräfte die auf das System wirken", "keywords": ["druck", "kraft", "einfluss"], "min_length": 50, "ideal_length": 150, "weight": 15},
    "tiefe": {"description": "Fundamentale Ebenen und Kernaspekte", "keywords": ["kern", "fundament", "essenz"], "min_length": 80, "ideal_length": 200, "weight": 20},
    "wirkung": {"description": "Effekte auf andere Systeme", "keywords": ["effekt", "wirkung", "resultat"], "min_length": 80, "ideal_length": 200, "weight": 20},
    "klartext": {"description": "Direkte Zusammenfassung", "keywords": ["klar", "direkt", "fazit"], "min_length": 30, "ideal_length": 100, "weight": 10}
}

SIGMA_FIELDS: Dict[str, Dict] = {
    "sigma_drift": {"description": "Σ-Drift: Systemdrift", "keywords": ["drift", "vektor"], "min_length": 50, "ideal_length": 150, "weight": 15},
    "sigma_mechanismus": {"description": "Σ-Mechanismus: Kernprozesse", "keywords": ["mechanismus", "prozess"], "min_length": 80, "ideal_length": 200, "weight": 20},
    "sigma_frequenz": {"description": "Σ-Frequenz: Rhythmen", "keywords": ["frequenz", "rhythmus"], "min_length": 50, "ideal_length": 150, "weight": 15},
    "sigma_dichte": {"description": "Σ-Dichte: Informationsdichte", "keywords": ["dichte", "konzentration"], "min_length": 80, "ideal_length": 200, "weight": 20},
    "sigma_strome": {"description": "Σ-Ströme: Flüsse", "keywords": ["strom", "fluss"], "min_length": 80, "ideal_length": 200, "weight": 20},
    "sigma_extrakt": {"description": "Σ-Extrakt: Kernaussage", "keywords": ["extrakt", "essenz"], "min_length": 30, "ideal_length": 100, "weight": 10}
}

def get_field_definition(field_name: str) -> Optional[Dict]:
    if field_name in SYNTEX_SYSTEM_FIELDS:
        return SYNTEX_SYSTEM_FIELDS[field_name]
    if field_name in HUMAN_READABLE_FIELDS:
        return HUMAN_READABLE_FIELDS[field_name]
    if field_name in SIGMA_FIELDS:
        return SIGMA_FIELDS[field_name]
    return None

def get_all_field_names(format_type: str = "SYNTEX_SYSTEM") -> List[str]:
    if format_type == "SYNTEX_SYSTEM":
        return list(SYNTEX_SYSTEM_FIELDS.keys())
    elif format_type == "HUMAN":
        return list(HUMAN_READABLE_FIELDS.keys())
    elif format_type == "SIGMA":
        return list(SIGMA_FIELDS.keys())
    return []

def get_field_weights(format_type: str = "SYNTEX_SYSTEM") -> Dict[str, int]:
    if format_type == "SYNTEX_SYSTEM":
        return {k: v["weight"] for k, v in SYNTEX_SYSTEM_FIELDS.items()}
    elif format_type == "HUMAN":
        return {k: v["weight"] for k, v in HUMAN_READABLE_FIELDS.items()}
    elif format_type == "SIGMA":
        return {k: v["weight"] for k, v in SIGMA_FIELDS.items()}
    return {}

if __name__ == "__main__":
    print("=== SYNTX FIELD DEFINITIONS ===")
    for name in SYNTEX_SYSTEM_FIELDS:
        print(f"  - {name}: weight={SYNTEX_SYSTEM_FIELDS[name]['weight']}")
    print("✅ Field Definitions OK")
