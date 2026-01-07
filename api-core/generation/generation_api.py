"""
🌊 SYNTX STROM-ORCHESTRATOR API
═══════════════════════════════════════════════════════════════════

ROUTEN-STRUKTUR (Alle mindestens 2 Ebenen):
- /strom/dispatch              → Ströme erzeugen
- /strom/status                → System-Status
- /felder/verfuegbar           → Alle Felder abrufen
- /kalibrierung/topics         → Topics verwalten (GET/PUT)
- /kalibrierung/styles         → Styles verwalten (GET/PUT)
- /kalibrierung/openai         → OpenAI-Parameter (GET/PUT)
- /kalibrierung/cron           → Cron-Jobs verwalten (GET/POST/DELETE)
- /resonanz/parameter          → Aktuelle Kalibrierung abrufen
"""
from fastapi import APIRouter, HTTPException, Body, Path
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from pathlib import Path as FilePath
import sys
import yaml
import subprocess

# Systemanbindung
sys.path.insert(0, '/opt/syntx-workflow-api-get-prompts')
sys.path.insert(0, '/opt/syntx-workflow-api-get-prompts/gpt_generator')

from config.config_loader import get_config, load_config
from gpt_generator.syntx_prompt_generator import generate_prompt

router = APIRouter(tags=["strom-orchestration"])

KALIBRIERUNGS_QUELLE = FilePath("/opt/syntx-config/configs/generator.yaml")


# ═══════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════

class StromParameter(BaseModel):
    """Parameter für Strom-Erzeugung"""
    felder_topics: Dict[str, float] = Field(default={})
    felder_styles: Dict[str, float] = Field(default={})
    strom_anzahl: int = Field(default=1, ge=1, le=50)
    sprache: str = Field(default="de")


class StromErgebnis(BaseModel):
    """Resultat eines erzeugten Stroms"""
    erfolg: bool
    topic: str
    style: str
    sprache: str
    strom_text: Optional[str] = None
    qualitaet: Optional[float] = None
    kosten: Optional[float] = None
    dauer_ms: Optional[int] = None


class KalibrierungOpenAI(BaseModel):
    """OpenAI Kalibrierungs-Parameter"""
    model: str = Field(default="gpt-4o")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    top_p: float = Field(default=1.0, ge=0.0, le=1.0)
    max_tokens: int = Field(default=500, ge=50, le=4000)
    max_refusal_retries: int = Field(default=3, ge=0, le=10)


class FeldTopicsUpdate(BaseModel):
    """Topics kalibrieren"""
    kategorie: str
    topics: List[str]
    aktion: str = Field(default="set")  # set/add/remove


class FeldStylesUpdate(BaseModel):
    """Styles kalibrieren"""
    styles: List[str]
    aktion: str = Field(default="set")


class ZeitSchleife(BaseModel):
    """Cron Job Definition"""
    name: str
    rhythmus: str  # Cron format
    wrapper: Optional[str] = None
    batch_groesse: int = Field(default=20, ge=1, le=100)
    typ: str = Field(default="consumer")


# ═══════════════════════════════════════════════════════════════════
# HELFER
# ═══════════════════════════════════════════════════════════════════

def kalibrierung_speichern(config_data: dict):
    """Speichert Config zurück"""
    with open(KALIBRIERUNGS_QUELLE, 'w', encoding='utf-8') as f:
        yaml.dump(config_data, f, allow_unicode=True, default_flow_style=False)


def kalibrierung_neu_laden():
    """Lädt Config neu"""
    from config.config_loader import _config_cache
    _config_cache.clear()
    return load_config('generator', force_reload=True)


# ═══════════════════════════════════════════════════════════════════
# STROM ENDPOINTS (Strom erzeugen + Status)
# ═══════════════════════════════════════════════════════════════════

@router.post("/strom/dispatch")
async def strom_dispatch(params: StromParameter = Body(...)):
    """
    ⚡ STROM ERZEUGEN
    
    Dispatcht kohärente Prompt-Ströme basierend auf Feld-Gewichtungen.
    """
    try:
        if not params.felder_topics or not params.felder_styles:
            raise HTTPException(status_code=400, detail="Topics und Styles required")
        
        resultate = []
        
        # Topic und Style mit höchster Gewichtung wählen
        topic = max(params.felder_topics.items(), key=lambda x: x[1])[0]
        style = max(params.felder_styles.items(), key=lambda x: x[1])[0]
        
        for i in range(params.strom_anzahl):
            result = generate_prompt(
                prompt=topic,
                style=style,
                temperature=0.7,
                max_tokens=500
            )
            
            strom = StromErgebnis(
                erfolg=result.get('success', False),
                topic=topic,
                style=style,
                sprache=params.sprache,
                strom_text=result.get('prompt_generated'),
                qualitaet=result.get('quality_score', {}).get('total_score') if result.get('quality_score') else None,
                kosten=result.get('cost', {}).get('total_cost') if result.get('cost') else None,
                dauer_ms=result.get('duration_ms')
            )
            resultate.append(strom)
        
        successful = sum(1 for r in resultate if r.erfolg)
        total_cost = sum(r.kosten for r in resultate if r.kosten)
        
        return {
            "status": "STROM_ERZEUGT",
            "anzahl": params.strom_anzahl,
            "erfolg": successful,
            "fehlgeschlagen": params.strom_anzahl - successful,
            "kosten_usd": round(total_cost, 4),
            "stroeme": [r.dict() for r in resultate]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/strom/status")
async def strom_status():
    """📊 STROM-SYSTEM STATUS"""
    try:
        topics = get_config('generator', 'topics')
        total_topics = sum(len(t) for t in topics.values())
        styles = get_config('generator', 'styles', 'available', default=[])
        
        return {
            "status": "STROM_SYSTEM_AKTIV",
            "felder_verfuegbar": {
                "topics": total_topics,
                "kategorien": len(topics),
                "styles": len(styles)
            },
            "model": get_config('generator', 'openai', 'model'),
            "max_stroeme_pro_anfrage": 50
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════════════════
# FELDER ENDPOINTS (Verfügbare Felder abrufen)
# ═══════════════════════════════════════════════════════════════════

@router.get("/felder/verfuegbar")
async def felder_verfuegbar():
    """
    🌊 VERFÜGBARE FELDER
    
    Zeigt alle semantischen Felder, Resonanz-Modi und Sprachen.
    """
    try:
        topics = get_config('generator', 'topics')
        styles = get_config('generator', 'styles', 'available', default=[])
        sprachen = get_config('generator', 'languages', 'enabled', default=['de'])
        
        return {
            "status": "FELDER_VERFUEGBAR",
            "semantische_felder": topics,
            "resonanz_modi": styles,
            "sprachen": sprachen
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════════════════
# KALIBRIERUNG/TOPICS
# ═══════════════════════════════════════════════════════════════════

@router.get("/kalibrierung/topics")
async def kalibrierung_topics_abrufen():
    """📚 TOPICS ABRUFEN"""
    try:
        topics = get_config('generator', 'topics')
        total = sum(len(t) for t in topics.values())
        
        return {
            "status": "TOPICS_GELADEN",
            "gesamt": total,
            "kategorien": len(topics),
            "topics": topics
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/kalibrierung/topics")
async def kalibrierung_topics_setzen(update: FeldTopicsUpdate):
    """
    ✏️ TOPICS KALIBRIEREN
    
    Aktionen: set/add/remove
    """
    try:
        config = kalibrierung_neu_laden()
        
        if 'topics' not in config:
            config['topics'] = {}
        
        if update.aktion == "set":
            config['topics'][update.kategorie] = update.topics
        elif update.aktion == "add":
            if update.kategorie not in config['topics']:
                config['topics'][update.kategorie] = []
            existing = set(config['topics'][update.kategorie])
            config['topics'][update.kategorie] = list(existing | set(update.topics))
        elif update.aktion == "remove":
            if update.kategorie in config['topics']:
                existing = set(config['topics'][update.kategorie])
                config['topics'][update.kategorie] = list(existing - set(update.topics))
        
        kalibrierung_speichern(config)
        kalibrierung_neu_laden()
        
        return {
            "status": "TOPICS_KALIBRIERT",
            "kategorie": update.kategorie,
            "aktion": update.aktion,
            "anzahl": len(config['topics'].get(update.kategorie, []))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════════════════
# KALIBRIERUNG/STYLES
# ═══════════════════════════════════════════════════════════════════

@router.get("/kalibrierung/styles")
async def kalibrierung_styles_abrufen():
    """🎨 STYLES ABRUFEN"""
    try:
        styles = get_config('generator', 'styles', 'available', default=[])
        default = get_config('generator', 'styles', 'default')
        
        return {
            "status": "STYLES_GELADEN",
            "anzahl": len(styles),
            "standard": default,
            "styles": styles
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/kalibrierung/styles")
async def kalibrierung_styles_setzen(update: FeldStylesUpdate):
    """✏️ STYLES KALIBRIEREN"""
    try:
        config = kalibrierung_neu_laden()
        
        if 'styles' not in config:
            config['styles'] = {'available': []}
        
        if update.aktion == "set":
            config['styles']['available'] = update.styles
        elif update.aktion == "add":
            existing = set(config['styles'].get('available', []))
            config['styles']['available'] = list(existing | set(update.styles))
        elif update.aktion == "remove":
            existing = set(config['styles'].get('available', []))
            config['styles']['available'] = list(existing - set(update.styles))
        
        kalibrierung_speichern(config)
        kalibrierung_neu_laden()
        
        return {
            "status": "STYLES_KALIBRIERT",
            "aktion": update.aktion,
            "anzahl": len(config['styles']['available'])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════════════════
# KALIBRIERUNG/OPENAI
# ═══════════════════════════════════════════════════════════════════

@router.get("/kalibrierung/openai")
async def kalibrierung_openai_abrufen():
    """⚙️ OPENAI CONFIG ABRUFEN"""
    try:
        openai = get_config('generator', 'openai')
        return {
            "status": "OPENAI_CONFIG_GELADEN",
            "config": openai
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/kalibrierung/openai")
async def kalibrierung_openai_setzen(config: KalibrierungOpenAI):
    """⚙️ OPENAI CONFIG SETZEN"""
    try:
        full_config = kalibrierung_neu_laden()
        
        full_config['openai'] = {
            'model': config.model,
            'temperature': config.temperature,
            'top_p': config.top_p,
            'max_tokens': config.max_tokens,
            'max_refusal_retries': config.max_refusal_retries
        }
        
        kalibrierung_speichern(full_config)
        kalibrierung_neu_laden()
        
        return {
            "status": "OPENAI_KALIBRIERT",
            "config": full_config['openai']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════════════════
# KALIBRIERUNG/CRON (Zeit-Schleifen)
# ═══════════════════════════════════════════════════════════════════

@router.get("/kalibrierung/cron")
async def kalibrierung_cron_abrufen():
    """⏰ ZEIT-SCHLEIFEN ABRUFEN"""
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        
        if result.returncode != 0:
            return {"status": "CRON_LEER", "schleifen": []}
        
        schleifen = []
        for line in result.stdout.split('\n'):
            line = line.strip()
            if line and not line.startswith('#') and 'syntx' in line.lower():
                schleifen.append({"raw": line, "aktiv": True})
        
        return {
            "status": "ZEIT_SCHLEIFEN_GELADEN",
            "anzahl": len(schleifen),
            "schleifen": schleifen
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/kalibrierung/cron")
async def kalibrierung_cron_hinzufuegen(schleife: ZeitSchleife):
    """
    ⏰ ZEIT-SCHLEIFE HINZUFÜGEN
    
    Typen:
    - producer: Erzeugt neue Ströme
    - consumer: Verarbeitet Queue
    """
    try:
        if schleife.typ == "producer":
            command = f"{schleife.rhythmus} /opt/syntx-workflow-api-get-prompts/crontab/run_producer.sh >> /opt/syntx-config/logs/producer_cron.log 2>&1"
        
        elif schleife.typ == "consumer":
            if not schleife.wrapper:
                raise HTTPException(status_code=400, detail="Consumer needs wrapper")
            
            command = f'{schleife.rhythmus} cd /opt/syntx-workflow-api-get-prompts && /usr/bin/python3 -c "from queue_system.core.consumer import QueueConsumer; c = QueueConsumer(\'{schleife.wrapper}\', \'cron_{schleife.name}\'); c.process_batch({schleife.batch_groesse})" >> /opt/syntx-config/logs/consumer_{schleife.wrapper}_cron.log 2>&1'
        
        else:
            raise HTTPException(status_code=400, detail="Invalid typ")
        
        # Crontab update
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        current = result.stdout if result.returncode == 0 else ""
        new_crontab = current.strip() + "\n" + command + "\n"
        
        process = subprocess.run(['crontab', '-'], input=new_crontab, text=True, capture_output=True)
        
        if process.returncode != 0:
            raise HTTPException(status_code=500, detail="Crontab update failed")
        
        return {
            "status": "ZEIT_SCHLEIFE_HINZUGEFUEGT",
            "name": schleife.name,
            "typ": schleife.typ,
            "rhythmus": schleife.rhythmus
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/kalibrierung/cron/{pattern}")
async def kalibrierung_cron_loeschen(pattern: str):
    """⏰ ZEIT-SCHLEIFE LÖSCHEN"""
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        
        if result.returncode != 0:
            return {"status": "CRON_LEER", "geloescht": 0}
        
        lines = result.stdout.split('\n')
        filtered = [line for line in lines if pattern not in line]
        deleted = len(lines) - len(filtered)
        
        new_crontab = '\n'.join(filtered)
        process = subprocess.run(['crontab', '-'], input=new_crontab, text=True, capture_output=True)
        
        if process.returncode != 0:
            raise HTTPException(status_code=500, detail="Crontab update failed")
        
        return {
            "status": "ZEIT_SCHLEIFE_GELOESCHT",
            "pattern": pattern,
            "geloescht": deleted
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════════════════
# RESONANZ/PARAMETER (Aktuelle Kalibrierung abrufen)
# ═══════════════════════════════════════════════════════════════════

@router.get("/resonanz/parameter")
async def resonanz_parameter():
    """
    🌊 RESONANZ-PARAMETER
    
    Zeigt die aktuelle System-Kalibrierung komplett.
    """
    try:
        config = get_config('generator')
        
        return {
            "status": "RESONANZ_PARAMETER_AKTIV",
            "openai": config.get('openai'),
            "topics": config.get('topics'),
            "styles": config.get('styles'),
            "languages": config.get('languages'),
            "batch": config.get('batch')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 🌊 TOPIC WEIGHTS ENDPOINTS
from .topic_weights_handler import (
    load_topic_weights,
    save_topic_weights,
    get_topic_weight,
    update_topic_weight
)

@router.get("/topic-weights")
async def get_topic_weights():
    """
    🌊 GET TOPIC WEIGHTS
    Hole alle gespeicherten Topic-Gewichtungen
    """
    try:
        weights = load_topic_weights()
        return {
            "erfolg": True,
            "weights": weights,
            "anzahl": len(weights)
        }
    except Exception as e:
        return {
            "erfolg": False,
            "fehler": str(e),
            "weights": {}
        }

@router.put("/topic-weights")
async def update_topic_weights(request: dict):
    """
    🌊 UPDATE TOPIC WEIGHTS
    Speichere Topic-Gewichtungen
    
    Body:
    {
        "weights": {
            "Quantencomputer": 0.8,
            "Künstliche Intelligenz": 0.9,
            ...
        }
    }
    """
    try:
        weights = request.get('weights', {})
        
        if not weights:
            return {
                "erfolg": False,
                "fehler": "Keine Gewichtungen übergeben"
            }
        
        # Validate weights (0-1)
        for topic, weight in weights.items():
            if not 0 <= weight <= 1:
                return {
                    "erfolg": False,
                    "fehler": f"Ungültige Gewichtung für {topic}: {weight} (muss 0-1 sein)"
                }
        
        success = save_topic_weights(weights)
        
        return {
            "erfolg": success,
            "gespeichert": len(weights),
            "message": f"✅ {len(weights)} Topic-Gewichtungen gespeichert"
        }
        
    except Exception as e:
        return {
            "erfolg": False,
            "fehler": str(e)
        }

@router.get("/topic-weights/{topic_name}")
async def get_single_topic_weight(topic_name: str):
    """
    🌊 GET SINGLE TOPIC WEIGHT
    Hole Gewichtung für ein einzelnes Topic
    """
    try:
        weight = get_topic_weight(topic_name)
        return {
            "erfolg": True,
            "topic": topic_name,
            "weight": weight
        }
    except Exception as e:
        return {
            "erfolg": False,
            "fehler": str(e)
        }

@router.put("/topic-weights/{topic_name}")
async def update_single_topic_weight(topic_name: str, request: dict):
    """
    🌊 UPDATE SINGLE TOPIC WEIGHT
    Update Gewichtung für ein einzelnes Topic
    
    Body:
    {
        "weight": 0.75
    }
    """
    try:
        weight = request.get('weight')
        
        if weight is None:
            return {
                "erfolg": False,
                "fehler": "Keine Gewichtung übergeben"
            }
        
        if not 0 <= weight <= 1:
            return {
                "erfolg": False,
                "fehler": f"Ungültige Gewichtung: {weight} (muss 0-1 sein)"
            }
        
        success = update_topic_weight(topic_name, weight)
        
        return {
            "erfolg": success,
            "topic": topic_name,
            "weight": weight,
            "message": f"✅ Gewichtung für {topic_name} auf {weight} gesetzt"
        }
        
    except Exception as e:
        return {
            "erfolg": False,
            "fehler": str(e)
        }

# Import extended handler
from .cron_extended_handler import (
    get_cron_logs,
    get_cron_stats,
    get_cron_by_id,
    update_cron_config,
    trigger_cron_manually,
    get_cron_impact
)

# ==========================================

# ==========================================
# KRONTUN ENDPOINTS
# ==========================================

# Import extended handler
try:
    from .cron_extended_handler import (
        get_cron_logs,
        get_cron_stats,
        get_cron_by_id,
        update_cron_config,
        trigger_cron_manually,
        get_cron_impact
    )
except ImportError:
    from cron_extended_handler import (
        get_cron_logs,
        get_cron_stats,
        get_cron_by_id,
        update_cron_config,
        trigger_cron_manually,
        get_cron_impact
    )


@router.get("/kalibrierung/cron/stats")
async def get_cron_statistics():
    """
    Echtzeit Stats für LiveQueueOverview
    """
    try:
        stats = get_cron_stats()
        return {
            "erfolg": True,
            **stats
        }
    except Exception as e:
        return {
            "erfolg": False,
            "fehler": str(e)
        }


@router.get("/kalibrierung/cron/logs")
async def get_cron_execution_logs(
    limit: int = 100,
    cron_id: str = None
):
    """
    Holt Cron Execution History
    """
    try:
        logs = get_cron_logs(limit=limit, cron_id=cron_id)
        return {
            "erfolg": True,
            "anzahl": len(logs),
            "logs": logs
        }
    except Exception as e:
        return {
            "erfolg": False,
            "fehler": str(e)
        }


@router.get("/kalibrierung/cron/impact")
async def get_cron_impact_analytics():
    """
    Impact Analytics für Heatmap
    Topics x Time = Prompt Count
    WICHTIG: Muss VOR /{cron_id} kommen!
    """
    try:
        impact = get_cron_impact()
        return {
            "erfolg": True,
            **impact
        }
    except Exception as e:
        return {
            "erfolg": False,
            "fehler": str(e)
        }


@router.get("/kalibrierung/cron/{cron_id}")
async def get_cron_details(cron_id: str):
    """
    Holt Details zu einem einzelnen Cron
    """
    try:
        details = get_cron_by_id(cron_id)
        
        if not details:
            return {
                "erfolg": False,
                "fehler": f"Cron {cron_id} nicht gefunden"
            }
        
        return {
            "erfolg": True,
            **details
        }
    except Exception as e:
        return {
            "erfolg": False,
            "fehler": str(e)
        }


@router.put("/kalibrierung/cron/{cron_id}")
async def update_cron(cron_id: str, updates: dict):
    """
    Updated einen Cron (Zeit, Felder, etc.)
    """
    try:
        success = update_cron_config(cron_id, updates)
        
        if success:
            return {
                "erfolg": True,
                "cron_id": cron_id,
                "message": "Cron erfolgreich aktualisiert",
                "updates": updates
            }
        else:
            return {
                "erfolg": False,
                "fehler": "Update fehlgeschlagen"
            }
    except Exception as e:
        return {
            "erfolg": False,
            "fehler": str(e)
        }


@router.post("/kalibrierung/cron/{cron_id}/run")
async def trigger_cron(cron_id: str):
    """
    Triggert einen Cron manuell
    """
    try:
        result = trigger_cron_manually(cron_id)
        return result
    except Exception as e:
        return {
            "erfolg": False,
            "fehler": str(e)
        }
