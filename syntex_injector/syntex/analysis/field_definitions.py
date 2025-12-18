"""
SYNTX Field Definitions - Dynamisch aus JSON oder Fallback auf Hardcoded
v2.1 - Mit Format Loader Integration
"""
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger("SYNTX.FieldDefinitions")

# === FORMAT LOADER INTEGRATION ===
# Versuche den Format Loader zu importieren
FORMAT_LOADER_AVAILABLE = False
_format_cache: Dict[str, Dict] = {}

try:
    # Add api-core to path if needed
    api_core_path = Path("/opt/syntx-workflow-api-get-prompts/api-core")
    if api_core_path.exists() and str(api_core_path) not in sys.path:
        sys.path.insert(0, str(api_core_path))
    
    from formats.format_loader import load_format, get_field_definitions
    FORMAT_LOADER_AVAILABLE = True
    logger.info("✅ Format Loader verfügbar - nutze JSON Definitionen")
except ImportError as e:
    logger.warning(f"⚠️ Format Loader nicht verfügbar, nutze Fallback: {e}")

# === FALLBACK: HARDCODED DEFINITIONS ===
# Diese werden nur genutzt wenn der Format Loader nicht verfügbar ist

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
    "sigma_hintergrund": {"description": "Σ-Hintergrund: Latente Muster", "keywords": ["muster", "latent"], "min_length": 80, "ideal_length": 200, "weight": 20},
    "sigma_druck": {"description": "Σ-Druck: Systemdruck", "keywords": ["druck", "spannung"], "min_length": 50, "ideal_length": 150, "weight": 15},
    "sigma_tiefe": {"description": "Σ-Tiefe: Systemtiefe", "keywords": ["tiefe", "fundament"], "min_length": 80, "ideal_length": 200, "weight": 20},
    "sigma_wirkung": {"description": "Σ-Wirkung: Systemwirkung", "keywords": ["wirkung", "effekt"], "min_length": 80, "ideal_length": 200, "weight": 20},
    "sigma_klartext": {"description": "Σ-Klartext: Klare Aussage", "keywords": ["klar", "fazit"], "min_length": 30, "ideal_length": 100, "weight": 10}
}

# Mapping für Format-Namen
FORMAT_NAME_MAP = {
    "SYNTEX_SYSTEM": "syntex_system",
    "syntex_system": "syntex_system",
    "HUMAN": "human",
    "human": "human",
    "SIGMA": "sigma",
    "sigma": "sigma"
}

FALLBACK_FIELDS = {
    "SYNTEX_SYSTEM": SYNTEX_SYSTEM_FIELDS,
    "syntex_system": SYNTEX_SYSTEM_FIELDS,
    "HUMAN": HUMAN_READABLE_FIELDS,
    "human": HUMAN_READABLE_FIELDS,
    "SIGMA": SIGMA_FIELDS,
    "sigma": SIGMA_FIELDS
}


def _load_format_from_json(format_type: str) -> Optional[Dict[str, Dict]]:
    """Lade Format aus JSON via Format Loader"""
    if not FORMAT_LOADER_AVAILABLE:
        return None
    
    # Normalisiere Format-Namen
    format_name = FORMAT_NAME_MAP.get(format_type, format_type.lower())
    
    # Check cache
    if format_name in _format_cache:
        return _format_cache[format_name]
    
    try:
        fields_data = get_field_definitions(format_name, language="de")
        if fields_data:
            # get_field_definitions gibt direkt das Dict zurück
            result = {}
            for field_name, field_def in fields_data.items():
                result[field_name] = {
                    "description": field_def.get("description", ""),
                    "keywords": field_def.get("keywords", []),
                    "min_length": field_def.get("min_length", 50),
                    "ideal_length": field_def.get("ideal_length", 200),
                    "weight": field_def.get("weight", 20),
                    "anti_keywords": field_def.get("anti_keywords", []),
                    "requires_tiers": field_def.get("requires_tiers", False)
                }
            _format_cache[format_name] = result
            logger.debug(f"✅ Format '{format_name}' aus JSON geladen: {len(result)} Felder")
            return result
    except Exception as e:
        logger.warning(f"⚠️ Konnte Format '{format_name}' nicht aus JSON laden: {e}")
    
    return None


def get_fields_for_format(format_type: str) -> Dict[str, Dict]:
    """Hole alle Feld-Definitionen für ein Format (JSON oder Fallback)"""
    # Versuche JSON
    json_fields = _load_format_from_json(format_type)
    if json_fields:
        return json_fields
    
    # Fallback auf hardcoded
    return FALLBACK_FIELDS.get(format_type, SYNTEX_SYSTEM_FIELDS)


def get_field_definition(field_name: str, format_type: str = None) -> Optional[Dict]:
    """Hole Definition für ein einzelnes Feld"""
    # Wenn format_type gegeben, nutze dieses
    if format_type:
        fields = get_fields_for_format(format_type)
        return fields.get(field_name)
    
    # Sonst suche in allen Formaten (Legacy-Verhalten)
    for fmt in ["SYNTEX_SYSTEM", "HUMAN", "SIGMA"]:
        fields = get_fields_for_format(fmt)
        if field_name in fields:
            return fields[field_name]
    
    return None


def get_all_field_names(format_type: str = "SYNTEX_SYSTEM") -> List[str]:
    """Hole alle Feld-Namen für ein Format"""
    fields = get_fields_for_format(format_type)
    return list(fields.keys())


def get_field_weights(format_type: str = "SYNTEX_SYSTEM") -> Dict[str, int]:
    """Hole alle Feld-Gewichtungen für ein Format"""
    fields = get_fields_for_format(format_type)
    return {k: v.get("weight", 20) for k, v in fields.items()}


def clear_format_cache():
    """Cache leeren (z.B. nach Format-Update)"""
    global _format_cache
    _format_cache = {}
    logger.info("🧹 Format-Cache geleert")


# === INFO LOGGING ===
if FORMAT_LOADER_AVAILABLE:
    logger.info("🌊 SYNTX Field Definitions v2.1 - JSON Mode")
else:
    logger.info("⚡ SYNTX Field Definitions v2.1 - Fallback Mode")
