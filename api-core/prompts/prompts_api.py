"""
SYNTX Prompts API
Clean flows. No patches. Field-based thinking.
"""
from fastapi import APIRouter, Query, HTTPException
from pathlib import Path
import json
from typing import Optional, Dict, List
from collections import defaultdict, Counter

router = APIRouter(prefix="/prompts", tags=["prompts"])

QUEUE_DIR = Path("/opt/syntx-workflow-api-get-prompts/queue")
LOGS_DIR = Path("/opt/syntx-workflow-api-get-prompts/logs")

# ============================================================================
# CORE HELPERS - THE FOUNDATION
# ============================================================================

def load_all_processed() -> List[Dict]:
    """Load all processed prompts - SAFE"""
    processed = []
    processed_dir = QUEUE_DIR / "processed"
    
    if not processed_dir.exists():
        return processed
    
    for file in processed_dir.glob("*.json"):
        try:
            with open(file) as f:
                data = json.load(f)
                if data and isinstance(data, dict):
                    processed.append(data)
        except:
            continue
    
    return processed

def safe_get_score(prompt: dict) -> float:
    """Extract score - SAFE"""
    try:
        result = prompt.get('syntex_result')
        if not result or not isinstance(result, dict):
            return 0.0
        
        quality = result.get('quality_score')
        if not quality or not isinstance(quality, dict):
            return 0.0
        
        score = quality.get('total_score', 0)
        return float(score) if score else 0.0
    except:
        return 0.0

def safe_get_fields(prompt: dict) -> Dict[str, bool]:
    """Extract field breakdown - SAFE"""
    try:
        result = prompt.get('syntex_result')
        if not result or not isinstance(result, dict):
            return {}
        
        quality = result.get('quality_score')
        if not quality or not isinstance(quality, dict):
            return {}
        
        breakdown = quality.get('detail_breakdown', {})
        return breakdown if isinstance(breakdown, dict) else {}
    except:
        return {}

# ============================================================================
# BASIC QUERIES
# ============================================================================

@router.get("/all")
async def get_all_prompts(limit: int = Query(100, le=500)):
    """Get all prompts metadata (no text)"""
    processed = load_all_processed()
    
    # Build clean metadata
    results = []
    for p in processed[:limit]:
        results.append({
            "id": p.get('filename', 'unknown'),
            "topic": p.get('topic', 'unknown'),
            "style": p.get('style', 'unknown'),
            "category": p.get('category', 'unknown'),
            "score": safe_get_score(p),
            "timestamp": p.get('processed_at', ''),
            "wrapper": p.get('syntex_result', {}).get('wrapper', 'unknown') if isinstance(p.get('syntex_result'), dict) else 'unknown'
        })
    
    return {
        "status": "ALL_PROMPTS",
        "total": len(results),
        "prompts": results
    }

@router.get("/by-job/{job_id}")
async def get_by_job(job_id: str):
    """Get specific job by ID"""
    processed = load_all_processed()
    
    for p in processed:
        if job_id in str(p.get('filename', '')):
            return {
                "status": "JOB_FOUND",
                "data": p
            }
    
    raise HTTPException(status_code=404, detail="Job not found")

@router.get("/best")
async def get_best_prompts(limit: int = Query(20, le=100)):
    """Best performing prompts"""
    processed = load_all_processed()
    
    # Sort by score
    sorted_prompts = sorted(processed, key=lambda p: safe_get_score(p), reverse=True)
    
    results = []
    for p in sorted_prompts[:limit]:
        results.append({
            "id": p.get('filename', 'unknown'),
            "topic": p.get('topic', 'unknown'),
            "score": safe_get_score(p),
            "fields": safe_get_fields(p),
            "timestamp": p.get('processed_at', '')
        })
    
    return {
        "status": "BEST_PROMPTS",
        "total": len(results),
        "prompts": results
    }

# ============================================================================
# ANALYTICS
# ============================================================================

@router.get("/fields/breakdown")
async def fields_breakdown():
    """Field completion analysis"""
    processed = load_all_processed()
    
    field_stats = {
        'drift': {'present': 0, 'absent': 0},
        'hintergrund_muster': {'present': 0, 'absent': 0},
        'druckfaktoren': {'present': 0, 'absent': 0},
        'tiefe': {'present': 0, 'absent': 0},
        'wirkung': {'present': 0, 'absent': 0},
        'klartext': {'present': 0, 'absent': 0}
    }
    
    for p in processed:
        fields = safe_get_fields(p)
        for field in field_stats.keys():
            if fields.get(field):
                field_stats[field]['present'] += 1
            else:
                field_stats[field]['absent'] += 1
    
    # Calculate rates
    for field, stats in field_stats.items():
        total = stats['present'] + stats['absent']
        stats['completion_rate'] = round(stats['present'] / total, 2) if total > 0 else 0
    
    return {
        "status": "FIELD_BREAKDOWN",
        "total_analyzed": len(processed),
        "fields": field_stats
    }

@router.get("/costs/total")
async def total_costs():
    """Total GPT costs"""
    processed = load_all_processed()
    
    total_cost = 0.0
    total_tokens = {"input": 0, "output": 0}
    
    for p in processed:
        cost_data = p.get('gpt_cost', {})
        if isinstance(cost_data, dict):
            total_cost += cost_data.get('total_cost', 0)
            total_tokens['input'] += cost_data.get('input_tokens', 0)
            total_tokens['output'] += cost_data.get('output_tokens', 0)
    
    return {
        "status": "COSTS_CALCULATED",
        "total_prompts": len(processed),
        "total_cost_usd": round(total_cost, 4),
        "total_tokens": total_tokens,
        "avg_cost_per_prompt": round(total_cost / len(processed), 4) if len(processed) > 0 else 0
    }

@router.get("/search")
async def search_prompts(q: str = Query(..., min_length=2)):
    """Search in prompts"""
    processed = load_all_processed()
    
    q_lower = q.lower()
    results = []
    
    for p in processed:
        # Search in topic, style, category
        searchable = f"{p.get('topic', '')} {p.get('style', '')} {p.get('category', '')}".lower()
        if q_lower in searchable:
            results.append({
                "id": p.get('filename', 'unknown'),
                "topic": p.get('topic', 'unknown'),
                "style": p.get('style', 'unknown'),
                "score": safe_get_score(p),
                "match": "metadata"
            })
    
    return {
        "status": "SEARCH_COMPLETE",
        "query": q,
        "total_results": len(results),
        "results": results
    }

# ============================================================================
# TABLE VIEW - OVERVIEW WITHOUT TEXT
# ============================================================================

@router.get("/table-view")
async def prompts_table_view(
    limit: int = Query(50, le=200),
    min_score: float = Query(0, ge=0, le=100),
    topic: Optional[str] = None
):
    """
    🔥 TABLE VIEW - Fast overview without full text
    Use /full-text/{id} to get complete prompt
    """
    
    processed = load_all_processed()
    
    # Filters
    if min_score > 0:
        processed = [p for p in processed if safe_get_score(p) >= min_score]
    
    if topic:
        processed = [p for p in processed if p.get('topic', '').lower() == topic.lower()]
    
    # Limit
    processed = processed[:limit]
    
    # Build table
    table = []
    for p in processed:
        # Get fields fulfilled
        fields = safe_get_fields(p)
        fields_fulfilled = [k for k, v in fields.items() if v]
        
        # Get wrapper safely
        wrapper = 'unknown'
        result = p.get('syntex_result')
        if result and isinstance(result, dict):
            wrapper = result.get('wrapper', 'unknown')
        
        # Get duration safely
        duration_ms = 0
        if result and isinstance(result, dict):
            duration_ms = result.get('duration_ms', 0)
        
        row = {
            "id": p.get('filename', 'unknown'),
            "timestamp": p.get('processed_at', ''),
            "topic": p.get('topic', 'unknown'),
            "style": p.get('style', 'unknown'),
            "category": p.get('category', 'unknown'),
            "score": safe_get_score(p),
            "fields_fulfilled": fields_fulfilled,
            "field_count": f"{len(fields_fulfilled)}/6",
            "duration_ms": duration_ms,
            "wrapper": wrapper
        }
        
        table.append(row)
    
    return {
        "status": "TABLE_VIEW_READY",
        "total_rows": len(table),
        "filters": {
            "min_score": min_score,
            "topic": topic,
            "limit": limit
        },
        "table": table
    }

# ============================================================================
# FULL TEXT - COMPLETE PROMPT DETAILS
# ============================================================================

@router.get("/full-text/{filename}")
async def get_full_prompt_text(filename: str):
    """
    📄 VOLLTEXT - Complete prompt & response for ONE file
    
    Use Case: User clicks row in table → loads details
    """
    
    # Find metadata file
    processed_file = QUEUE_DIR / "processed" / filename
    if not processed_file.exists() and not filename.endswith('.json'):
        processed_file = QUEUE_DIR / "processed" / f"{filename}.json"
    
    if not processed_file.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {filename}")
    
    # Load metadata
    with open(processed_file) as f:
        data = json.load(f)
    
    # Load prompt text file
    prompt_text = ""
    txt_filename = data.get('filename', '')
    if txt_filename:
        prompt_file = QUEUE_DIR / "processed" / txt_filename
        if prompt_file.exists():
            try:
                with open(prompt_file) as f:
                    prompt_text = f.read()
            except Exception as e:
                prompt_text = f"[Error reading file: {e}]"
        else:
            prompt_text = f"[Prompt file not found: {txt_filename}]"
    
    # Get response (if stored)
    response_text = "[Response not stored in metadata]"
    result = data.get('syntex_result')
    if result and isinstance(result, dict):
        response_text = result.get('response_text', response_text)
    
    return {
        "status": "FULL_TEXT_LOADED",
        "filename": filename,
        "topic": data.get('topic', 'unknown'),
        "style": data.get('style', 'unknown'),
        "category": data.get('category', 'unknown'),
        "score": safe_get_score(data),
        "timestamp": data.get('processed_at', ''),
        "prompt_full_text": prompt_text,
        "response_full_text": response_text,
        "fields_breakdown": safe_get_fields(data),
        "duration_ms": result.get('duration_ms', 0) if result and isinstance(result, dict) else 0,
        "wrapper": result.get('wrapper', 'unknown') if result and isinstance(result, dict) else 'unknown',
        "gpt_quality": data.get('gpt_quality', {}),
        "gpt_cost": data.get('gpt_cost', {})
    }

