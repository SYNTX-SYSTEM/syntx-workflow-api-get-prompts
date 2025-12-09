from fastapi import APIRouter
from utils.log_loader import load_field_flow
from datetime import datetime

router = APIRouter(prefix="/strom", tags=["strom"])

@router.get("/health")
async def strom_health():
    """Health check for the stream processing layer."""
    return {"status": "STROM_ONLINE", "timestamp": datetime.now().isoformat()}

@router.get("/queue/status")
async def strom_queue_status():
    """Placeholder for stream queue status."""
    entries = load_field_flow()
    total_processed = len(entries)
    
    return {
        "status": "QUEUE_READY",
        "processed_today": total_processed,
        "queue_depth": 0 # Assuming queue is empty after processing
    }
