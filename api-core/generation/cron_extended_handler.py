"""
SYNTX KRONTUN - Extended Cron Handler
Logs, Impact Analytics, Individual Cron Management
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import uuid

# Paths
CRON_LOGS_DIR = Path("/opt/syntx-config/logs/cron")
CRON_LOGS_DIR.mkdir(parents=True, exist_ok=True)

CRON_HISTORY_FILE = CRON_LOGS_DIR / "cron_history.jsonl"
CRON_IMPACT_FILE = CRON_LOGS_DIR / "cron_impact.json"


def log_cron_execution(cron_id: str, cron_data: dict, result: dict):
    """
    Loggt jeden Cron Run
    """
    log_entry = {
        "cron_id": cron_id,
        "timestamp": datetime.now().isoformat(),
        "cron_data": cron_data,
        "result": result
    }
    
    with open(CRON_HISTORY_FILE, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')


def get_cron_logs(limit: int = 100, cron_id: Optional[str] = None) -> List[dict]:
    """
    Holt Cron Execution Logs
    """
    if not CRON_HISTORY_FILE.exists():
        return []
    
    logs = []
    with open(CRON_HISTORY_FILE, 'r') as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                if cron_id is None or entry.get('cron_id') == cron_id:
                    logs.append(entry)
            except:
                continue
    
    # Return latest first
    logs = logs[-limit:]
    logs.reverse()
    
    return logs


def get_cron_stats() -> dict:
    """
    Berechnet Stats für LiveQueueOverview
    """
    logs = get_cron_logs(limit=1000)
    
    active = 0
    pending = 0
    completed = 0
    failed = 0
    
    for log in logs:
        result = log.get('result', {})
        status = result.get('status', 'pending')
        
        if status == 'active' or status == 'running':
            active += 1
        elif status == 'pending' or status == 'queued':
            pending += 1
        elif status == 'completed' or status == 'success':
            completed += 1
        elif status == 'failed' or status == 'error':
            failed += 1
    
    return {
        "active": active,
        "pending": pending,
        "completed": completed,
        "failed": failed,
        "total": len(logs)
    }


def get_cron_by_id(cron_id: str) -> Optional[dict]:
    """
    Holt Details zu einem einzelnen Cron
    """
    logs = get_cron_logs(cron_id=cron_id)
    
    if not logs:
        return None
    
    # Latest run
    latest = logs[0]
    
    # Aggregate all runs
    all_runs = []
    total_generated = 0
    total_failed = 0
    total_cost = 0.0
    
    for log in logs:
        result = log.get('result', {})
        all_runs.append({
            "timestamp": log.get('timestamp'),
            "status": result.get('status'),
            "generated": result.get('generated', 0),
            "failed": result.get('failed', 0),
            "cost": result.get('cost', 0.0)
        })
        
        total_generated += result.get('generated', 0)
        total_failed += result.get('failed', 0)
        total_cost += result.get('cost', 0.0)
    
    return {
        "cron_id": cron_id,
        "latest_run": latest,
        "all_runs": all_runs,
        "summary": {
            "total_runs": len(logs),
            "total_generated": total_generated,
            "total_failed": total_failed,
            "total_cost": round(total_cost, 4),
            "avg_generated": round(total_generated / len(logs), 2) if logs else 0
        }
    }


def update_cron_config(cron_id: str, updates: dict) -> bool:
    """
    Updated einen Cron (Zeit, Felder, etc.)
    Placeholder - wird später mit YAML Config verbunden
    """
    # TODO: Update generator.yaml
    return True


def trigger_cron_manually(cron_id: str) -> dict:
    """
    Triggert einen Cron manuell
    Placeholder - wird später mit actual cron execution verbunden
    """
    # TODO: Trigger actual cron job
    return {
        "erfolg": True,
        "cron_id": cron_id,
        "message": "Cron manuell getriggert",
        "timestamp": datetime.now().isoformat()
    }


def get_cron_impact() -> dict:
    """
    Berechnet Impact Analytics (Heatmap Data)
    Topics x Time = Prompt Count
    """
    logs = get_cron_logs(limit=1000)
    
    # Topics x Hour
    impact_matrix = {}
    
    for log in logs:
        timestamp = log.get('timestamp', '')
        try:
            dt = datetime.fromisoformat(timestamp)
            hour = dt.hour
        except:
            continue
        
        cron_data = log.get('cron_data', {})
        felder = cron_data.get('felder', {})
        result = log.get('result', {})
        generated = result.get('generated', 0)
        
        for topic, weight in felder.items():
            if topic not in impact_matrix:
                impact_matrix[topic] = [0] * 24
            
            # Weighted prompt count
            impact_matrix[topic][hour] += int(generated * weight)
    
    return {
        "impact_matrix": impact_matrix,
        "total_topics": len(impact_matrix),
        "time_range": "Last 1000 runs"
    }
