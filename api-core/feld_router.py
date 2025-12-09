from fastapi import APIRouter
from utils.log_loader import load_field_flow
from collections import Counter

router = APIRouter(prefix="/feld", tags=["feld"])

@router.get("/topics")
async def feld_topics():
    """Returns a count of topics in the field flow."""
    entries = load_field_flow()
    topics = [e.get('topic', 'unknown') for e in entries]
    
    return {
        "status": "TOPICS_AKTIV",
        "topic_counts": dict(Counter(topics))
    }

@router.get("/prompts")
async def feld_prompts():
    """Placeholder for field prompt analysis."""
    entries = load_field_flow()
    prompt_ids = [e.get('prompt_id') for e in entries if e.get('prompt_id')]
    
    return {
        "status": "PROMPTS_AKTIV",
        "total_prompts": len(prompt_ids),
        "unique_prompts": len(set(prompt_ids))
    }
