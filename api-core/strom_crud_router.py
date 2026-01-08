"""
🌊 SYNTX STROM CRUD ROUTER
Complete CRUD for Calibration Streams (First-Class Entities)

SYNTX Terminologie:
- strom = calibration stream/flow
- feld = semantic field
- kalibrierung = calibration
- muster = pattern identifier
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from pathlib import Path
from datetime import datetime
import yaml
import uuid

router = APIRouter(prefix="/strom/crud", tags=["strom-crud"])

# ============================================
# 💎 STORAGE PATH
# ============================================
STROEME_PATH = Path("/opt/syntx-config/stroeme/stroeme.yaml")

# ============================================
# 🔥 PYDANTIC MODELS
# ============================================

class StromCreate(BaseModel):
    """Create a new calibration stream"""
    name: str = Field(..., description="Human-readable name")
    zeitplan: str = Field(..., description="Cron schedule expression")
    modell: str = Field(default="gpt-4o", description="AI model to use")
    felder_topics: Dict[str, float] = Field(default_factory=dict, description="Field weights")
    styles: List[str] = Field(default_factory=lambda: ["technisch"], description="Style preferences")
    sprachen: List[str] = Field(default_factory=lambda: ["de"], description="Languages")
    aktiv: bool = Field(default=True, description="Active status")

class StromUpdate(BaseModel):
    """Update existing calibration stream"""
    name: Optional[str] = None
    zeitplan: Optional[str] = None
    modell: Optional[str] = None
    felder_topics: Optional[Dict[str, float]] = None
    styles: Optional[List[str]] = None
    sprachen: Optional[List[str]] = None
    aktiv: Optional[bool] = None

class StromResponse(BaseModel):
    """Stream response model"""
    strom_id: str
    muster: str
    name: str
    zeitplan: str
    modell: str
    felder_topics: Dict[str, float]
    styles: List[str]
    sprachen: List[str]
    aktiv: bool
    created_at: str
    updated_at: str

# ============================================
# 🌊 YAML HELPER FUNCTIONS
# ============================================

def _load_stroeme() -> dict:
    """Load stroeme.yaml"""
    if not STROEME_PATH.exists():
        return {"stroeme": {}}
    
    with open(STROEME_PATH, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    return data if data else {"stroeme": {}}

def _save_stroeme(data: dict):
    """Save stroeme.yaml"""
    STROEME_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    with open(STROEME_PATH, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

def _generate_muster(name: str) -> str:
    """Generate pattern identifier from name"""
    return name.lower().replace(' ', '_').replace('-', '_')

# ============================================
# 1️⃣ CREATE - POST /strom
# ============================================

@router.post("", response_model=StromResponse)
async def create_strom(strom: StromCreate):
    """
    🔥 CREATE new calibration stream
    
    Example:
        POST /strom
        {
            "name": "Evening Analysis Flow",
            "zeitplan": "0 18 * * *",
            "modell": "gpt-4o",
            "felder_topics": {"bildung": 0.8, "technologie": 0.6},
            "styles": ["technisch", "akademisch"],
            "sprachen": ["de", "en"]
        }
    """
    try:
        # Load current stroeme
        data = _load_stroeme()
        
        # Generate IDs
        strom_id = f"strom_{uuid.uuid4().hex[:8]}"
        muster = _generate_muster(strom.name)
        
        # Check if muster already exists
        if muster in data['stroeme']:
            raise HTTPException(
                status_code=409, 
                detail=f"Strom mit Muster '{muster}' existiert bereits"
            )
        
        # Create timestamp
        now = datetime.now().isoformat()
        
        # Build strom object
        new_strom = {
            "strom_id": strom_id,
            "name": strom.name,
            "zeitplan": strom.zeitplan,
            "modell": strom.modell,
            "felder_topics": strom.felder_topics,
            "styles": strom.styles,
            "sprachen": strom.sprachen,
            "aktiv": strom.aktiv,
            "created_at": now,
            "updated_at": now
        }
        
        # Add to stroeme
        data['stroeme'][muster] = new_strom
        
        # Save
        _save_stroeme(data)
        
        return StromResponse(muster=muster, **new_strom)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Erstellen: {str(e)}")

# ============================================
# 2️⃣ READ - GET /strom
# ============================================

@router.get("", response_model=List[StromResponse])
async def list_stroeme(aktiv_only: bool = False):
    """
    💎 LIST all calibration streams
    
    Query params:
        aktiv_only: Only return active streams
    
    Example:
        GET /strom
        GET /strom?aktiv_only=true
    """
    try:
        data = _load_stroeme()
        
        stroeme = []
        for muster, strom_data in data.get('stroeme', {}).items():
            # Filter by aktiv status
            if aktiv_only and not strom_data.get('aktiv', True):
                continue
            
            stroeme.append(
                StromResponse(muster=muster, **strom_data)
            )
        
        return stroeme
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Laden: {str(e)}")

# ============================================
# 2️⃣.1 READ SINGLE - GET /strom/{muster}
# ============================================

@router.get("/{muster}", response_model=StromResponse)
async def get_strom(muster: str):
    """
    💎 GET single calibration stream by pattern
    
    Example:
        GET /strom/evening_analysis_flow
    """
    try:
        data = _load_stroeme()
        
        if muster not in data.get('stroeme', {}):
            raise HTTPException(status_code=404, detail=f"Strom '{muster}' nicht gefunden")
        
        strom_data = data['stroeme'][muster]
        
        return StromResponse(muster=muster, **strom_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler: {str(e)}")

# ============================================
# 3️⃣ UPDATE - PUT /strom/{muster}
# ============================================

@router.put("/{muster}", response_model=StromResponse)
async def update_strom(muster: str, update: StromUpdate):
    """
    ⚡ UPDATE existing calibration stream
    
    Example:
        PUT /strom/evening_analysis_flow
        {
            "zeitplan": "0 20 * * *",
            "felder_topics": {"bildung": 0.9}
        }
    """
    try:
        # Load stroeme
        data = _load_stroeme()
        
        # Check if exists
        if muster not in data.get('stroeme', {}):
            raise HTTPException(status_code=404, detail=f"Strom '{muster}' nicht gefunden")
        
        strom = data['stroeme'][muster]
        
        # Update fields (only if provided)
        if update.name is not None:
            strom['name'] = update.name
        if update.zeitplan is not None:
            strom['zeitplan'] = update.zeitplan
        if update.modell is not None:
            strom['modell'] = update.modell
        if update.felder_topics is not None:
            strom['felder_topics'] = update.felder_topics
        if update.styles is not None:
            strom['styles'] = update.styles
        if update.sprachen is not None:
            strom['sprachen'] = update.sprachen
        if update.aktiv is not None:
            strom['aktiv'] = update.aktiv
        
        # Update timestamp
        strom['updated_at'] = datetime.now().isoformat()
        
        # Save
        _save_stroeme(data)
        
        return StromResponse(muster=muster, **strom)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Aktualisieren: {str(e)}")

# ============================================
# 4️⃣ DELETE - DELETE /strom/{muster}
# ============================================

@router.delete("/{muster}")
async def delete_strom(muster: str):
    """
    🔥 DELETE calibration stream
    
    Note: Only removes definition, logs remain intact
    
    Example:
        DELETE /strom/evening_analysis_flow
    """
    try:
        # Load stroeme
        data = _load_stroeme()
        
        # Check if exists
        if muster not in data.get('stroeme', {}):
            raise HTTPException(status_code=404, detail=f"Strom '{muster}' nicht gefunden")
        
        # Remove strom
        deleted_strom = data['stroeme'].pop(muster)
        
        # Save
        _save_stroeme(data)
        
        return {
            "erfolg": True,
            "status": "gelöscht",
            "muster": muster,
            "strom_id": deleted_strom.get('strom_id')
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Löschen: {str(e)}")
