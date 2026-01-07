"""
🌊 SYNTX TOPIC WEIGHTS HANDLER
Speichert und lädt Topic-Gewichtungen für Field Control
"""

import json
import os
from pathlib import Path
from typing import Dict
from datetime import datetime

WEIGHTS_FILE = Path("/opt/syntx-config/configs/topic_weights.json")

def load_topic_weights() -> Dict[str, float]:
    """Lade gespeicherte Topic-Gewichtungen"""
    if not WEIGHTS_FILE.exists():
        return {}
    
    try:
        with open(WEIGHTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('weights', {})
    except Exception as e:
        print(f"❌ Failed to load topic weights: {e}")
        return {}

def save_topic_weights(weights: Dict[str, float]) -> bool:
    """Speichere Topic-Gewichtungen"""
    try:
        # Ensure directory exists
        WEIGHTS_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        # Prepare data
        data = {
            'weights': weights,
            'last_updated': datetime.now().isoformat(),
            'total_topics': len(weights)
        }
        
        # Write to file
        with open(WEIGHTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved {len(weights)} topic weights to {WEIGHTS_FILE}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to save topic weights: {e}")
        return False

def get_topic_weight(topic_name: str) -> float:
    """Hole Gewichtung für ein einzelnes Topic (default: 0.5)"""
    weights = load_topic_weights()
    return weights.get(topic_name, 0.5)

def update_topic_weight(topic_name: str, weight: float) -> bool:
    """Update einzelnes Topic Weight"""
    weights = load_topic_weights()
    weights[topic_name] = max(0.0, min(1.0, weight))  # Clamp to 0-1
    return save_topic_weights(weights)
