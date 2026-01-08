from fastapi import APIRouter, Query
from pathlib import Path
import json
from datetime import datetime

router = APIRouter(prefix="/kalibrierung", tags=["kalibrierung"])

@router.get("/cron/logs")
async def get_cron_logs(limit: int = Query(100, le=500)):
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
                    
                    # Extract cron info with VOLLTEXT stages
                    log = {
                        "cron_id": f"calibration-{data['timestamp'][:19]}",
                        "timestamp": data['timestamp'],
                        "cron_data": {
                            "name": f"{data['system']} Calibration",
                            "modell": "mistral-uncensored",
                            "anzahl": 1,
                            "felder": _extract_fields(data)
                        },
                        # 🔥 VOLLTEXT STAGES with GPT USER PROMPT!
                        "stages": {
                            "gpt_system_prompt": data.get('system', ''),
                            "gpt_user_prompt": data.get('gpt_user_prompt', ''),  # 🔥 NEU!
                            "gpt_output_meta_prompt": data.get('meta_prompt', ''),
                            "mistral_input": data.get('meta_prompt', ''),
                            "mistral_output": data.get('response', ''),
                            "parsed_fields": data.get('parsed_fields', {})
                        },
                        "result": {
                            "status": "completed" if data['success'] else "failed",
                            "generated": 1 if data['success'] else 0,
                            "failed": 0 if data['success'] else 1,
                            "avg_quality": data.get('quality_score', {}).get('total_score', 0),
                            "drift": _calculate_drift(data),
                            "cost": data.get('cost', 0.01),
                            "duration_ms": data.get('duration_ms', 0)
                        }
                    }
                    logs.append(log)
                except:
                    continue
        
        # Sort by timestamp (newest first)
        logs.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return {
            "erfolg": True,
            "anzahl": min(limit, len(logs)),
            "logs": logs[:limit]
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

def _extract_fields(data: dict) -> dict:
    """Extract field weights from parsed_fields"""
    parsed = data.get('parsed_fields', {})
    if not parsed:
        return {"DRIFT": 1, "HINTERGRUND-MUSTER": 1, "DRUCKFAKTOREN": 1}
    
    fields = {}
    for key in parsed.keys():
        fields[key] = 1
    
    return fields if fields else {"DRIFT": 1, "HINTERGRUND-MUSTER": 1, "DRUCKFAKTOREN": 1}

def _calculate_drift(data: dict) -> float:
    """Calculate drift percentage from quality score"""
    quality = data.get('quality_score', {}).get('total_score', 0)
    return max(0.0, (100 - quality) / 100)
