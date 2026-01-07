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
                    
                    # Extract cron info
                    log = {
                        "cron_id": f"calibration-{data['timestamp'][:19]}",
                        "timestamp": data['timestamp'],
                        "cron_data": {
                            "name": f"{data['system']} Calibration",
                            "modell": "mistral-uncensored",
                            "anzahl": 1,
                            "felder": _extract_fields(data)
                        },
                        "result": {
                            "status": "completed" if data['success'] else "failed",
                            "generated": 1 if data['success'] else 0,
                            "failed": 0 if data['success'] else 1,
                            "avg_quality": data.get('quality_score', {}).get('total_score', 0),
                            "drift": _calculate_drift(data),
                            "cost": 0.01,
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

@router.get("/cron/impact")
async def get_cron_impact():
    """Get topic impact from calibrations"""
    return {
        "erfolg": True,
        "impact": []
    }

def _extract_fields(data: dict) -> dict:
    """Extract field weights from calibration data"""
    fields = {}
    parsed = data.get('parsed_fields', {})
    
    # Count which fields are present and not null
    field_names = ['drift', 'hintergrund_muster', 'druckfaktoren', 'tiefe', 'wirkung', 'klartext']
    for field in field_names:
        value = parsed.get(field)
        if value and isinstance(value, str) and len(value.strip()) > 0:
            # Use human-readable names
            readable_name = field.replace('_', ' ').replace('hintergrund muster', 'Hintergrund-Muster').title()
            fields[readable_name] = 1.0
    
    # If no fields found, check detail_breakdown from quality_score
    if not fields:
        quality = data.get('quality_score', {})
        breakdown = quality.get('detail_breakdown', {})
        for field, present in breakdown.items():
            if present:
                readable_name = field.replace('_', ' ').title()
                fields[readable_name] = 1.0
    
    return fields if fields else {"Unknown": 1.0}

def _calculate_drift(data: dict) -> float:
    """Calculate drift from quality score"""
    quality = data.get('quality_score', {})
    total_score = quality.get('total_score', 0)
    
    # Drift is inverse of quality (0-1 scale)
    if total_score >= 90:
        return 0.05
    elif total_score >= 70:
        return 0.15
    elif total_score >= 50:
        return 0.25
    else:
        return 0.40
