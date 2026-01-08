"""
🔥 KALIBRIERUNG ROUTER - PHASE 1: STROM UPDATE
SYNTX Terminologie im Code
"""
from fastapi import APIRouter, Query, HTTPException
from pathlib import Path
from pydantic import BaseModel
from typing import Optional, Dict, List
import json
import yaml
from datetime import datetime

router = APIRouter(prefix="/kalibrierung", tags=["kalibrierung"])

# ============================================
# 💎 PYDANTIC MODELS (SYNTX Terminologie)
# ============================================

class StromUpdate(BaseModel):
    """Update data for a calibration stream (cron)"""
    zeitplan: Optional[str] = None  # Cron pattern
    felder_topics: Optional[Dict[str, float]] = None  # Field weights
    styles: Optional[List[str]] = None
    model: Optional[str] = None
    sprachen: Optional[List[str]] = None  # Languages

# ============================================
# 🔥 YAML HELPER FUNCTIONS
# ============================================

def _load_generator_yaml() -> dict:
    """Load generator.yaml"""
    yaml_path = Path("/opt/syntx-config/configs/generator.yaml")
    if not yaml_path.exists():
        raise FileNotFoundError("generator.yaml not found")
    
    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def _save_generator_yaml(data: dict):
    """Save generator.yaml"""
    yaml_path = Path("/opt/syntx-config/configs/generator.yaml")
    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)

# ============================================
# 🌊 EXISTING ENDPOINTS (from current router)
# ============================================

@router.get("/cron/logs")
async def get_cron_logs(limit: int = Query(100, le=1000)):
    """Get real calibration logs from syntex_calibrations.jsonl"""
    try:
        calibrations_file = Path("/opt/syntx-config/generator-data/syntex_calibrations.jsonl")
        
        if not calibrations_file.exists():
            return {"erfolg": False, "fehler": "Calibrations file not found"}
        
        logs = []
        with open(calibrations_file, 'r') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    
                    log = {
                        "timestamp": data['timestamp'],
                        "cron_data": {
                            "name": f"{data.get('system', 'SYNTEX')} Calibration",
                            "modell": "mistral-uncensored",
                            "felder": _extract_fields(data)
                        },
                        "stages": {
                            "gpt_system_prompt": data.get('system', ''),
                            "gpt_user_prompt": data.get('gpt_user_prompt', ''),
                            "gpt_output_meta_prompt": data.get('meta_prompt', ''),
                            "mistral_input": data.get('meta_prompt', ''),
                            "mistral_output": data.get('response', ''),
                            "parsed_fields": data.get('parsed_fields', {})
                        },
                        "scores": {
                            "overall": data.get('quality_score', {}).get('total_score', 0),
                            "field_completeness": data.get('quality_score', {}).get('field_completeness', 0),
                            "structure_adherence": data.get('quality_score', {}).get('structure_adherence', 0)
                        },
                        "meta": {
                            "duration_ms": data.get('duration_ms', 0),
                            "retry_count": data.get('retry_count', 0),
                            "success": data.get('success', False)
                        }
                    }
                    logs.append(log)
                except:
                    continue
        
        logs.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return {
            "erfolg": True,
            "logs": logs[:limit],
            "count": min(limit, len(logs)),
            "total": len(logs)
        }
        
    except Exception as e:
        return {"erfolg": False, "fehler": str(e)}

@router.get("/cron/stats")
async def get_cron_stats():
    """Get stats from calibrations"""
    try:
        calibrations_file = Path("/opt/syntx-config/generator-data/syntex_calibrations.jsonl")
        
        if not calibrations_file.exists():
            return {"erfolg": False}
        
        total = 0
        completed = 0
        failed = 0
        
        with open(calibrations_file, 'r') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    total += 1
                    if data.get('success'):
                        completed += 1
                    else:
                        failed += 1
                except:
                    continue
        
        return {
            "erfolg": True,
            "active": 0,
            "pending": 0,
            "completed": completed,
            "failed": failed,
            "total": total
        }
        
    except Exception as e:
        return {"erfolg": False}

# ============================================
# ⚡ NEW: PHASE 1 - STROM UPDATE ENDPOINT
# ============================================

@router.put("/strom/{muster}")
async def update_kalibrierungs_strom(muster: str, update_data: StromUpdate):
    """
    🔥 PHASE 1: Update existing calibration stream (cron)
    
    SYNTX Terminologie:
    - strom = calibration flow/stream
    - muster = cron pattern identifier
    - felder = semantic fields
    - zeitplan = schedule (cron expression)
    
    Args:
        muster: Pattern identifier (e.g., "morning_run")
        update_data: Fields to update
        
    Returns:
        Success response with updated data
        
    Example:
        PUT /kalibrierung/strom/morning_run
        {
            "zeitplan": "0 8 * * 1-5",
            "felder_topics": {"systemstruktur": 0.9},
            "styles": ["technisch"],
            "model": "gpt-4o"
        }
    """
    try:
        # Load current YAML
        config = _load_generator_yaml()
        
        # Check if crons section exists
        if 'crons' not in config:
            raise HTTPException(status_code=404, detail=f"Keine Crons in generator.yaml")
        
        # Find cron by pattern
        if muster not in config['crons']:
            raise HTTPException(status_code=404, detail=f"Kalibrierungs-Strom '{muster}' nicht gefunden")
        
        # Get current cron data
        cron = config['crons'][muster]
        
        # Update fields if provided
        if update_data.zeitplan is not None:
            cron['schedule'] = update_data.zeitplan
        
        if update_data.felder_topics is not None:
            if 'topics' not in cron:
                cron['topics'] = {}
            cron['topics'] = update_data.felder_topics
        
        if update_data.styles is not None:
            cron['styles'] = update_data.styles
        
        if update_data.model is not None:
            cron['model'] = update_data.model
        
        if update_data.sprachen is not None:
            cron['languages'] = update_data.sprachen
        
        # Add metadata
        cron['updated_at'] = datetime.now().isoformat()
        
        # Save updated YAML
        _save_generator_yaml(config)
        
        return {
            "erfolg": True,
            "status": "aktualisiert",
            "muster": muster,
            "strom": cron
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Aktualisieren: {str(e)}")

# ============================================
# 💎 HELPER FUNCTIONS
# ============================================

def _extract_fields(data: dict) -> dict:
    """Extract field weights from parsed_fields"""
    parsed = data.get('parsed_fields', {})
    if not parsed:
        return {"DRIFT": 1, "HINTERGRUND-MUSTER": 1, "DRUCKFAKTOREN": 1}
    
    fields = {}
    for key in parsed.keys():
        fields[key] = 1
    
    return fields if fields else {"DRIFT": 1, "HINTERGRUND-MUSTER": 1, "DRUCKFAKTOREN": 1}
