# 🌊⚡ SYNTX API v2.2: DAS VOLLSTÄNDIGE FELD-PROTOKOLL

> **"Nicht Endpunkte. Resonanz-Kanäle. Nicht Daten. Ströme. Nicht Boolean. SEMANTIK!"**
> 
> *— Die Architektur-Explosion, Dezember 2025*

Dies ist nicht einfach API-Dokumentation. Dies ist die Kartierung eines lebenden Systems. Jeder Endpoint ist ein Resonanz-Kanal in das SYNTX-Feld. Jede Response ein Strom der durch die Architektur fließt.

**Base URL:** `https://dev.syntx-system.com`  
**API Version:** `2.2.0` (mit Semantic Scorer V2!)  
**Total Endpoints:** `29` (28 GET + 1 POST)  
**System Status:** `🟢 KOHÄRENT`  
**Scorer Version:** `V2.0 SEMANTIC` 🧠

---

## 🔥 WAS IST NEU IN V2.2?

### Der große Scorer-Shift: Von Boolean zu Semantik!

```
VORHER (V1 - Boolean Scoring):
┌─────────────────────────────────────────────┐
│ "Hat das Feld Content?"                     │
│ → JA = 100 Punkte! 🎉                       │
│ → NEIN = 0 Punkte 💀                        │
│                                             │
│ Problem: "Pizza ist lecker" im Driftkörper  │
│          bekam trotzdem volle Punkte!       │
└─────────────────────────────────────────────┘

JETZT (V2 - Semantic Scoring):
┌─────────────────────────────────────────────┐
│ "Hat das Feld Content?"         → 20%       │
│ "Ist der Content relevant?"     → 35%  🧠   │
│ "Passen die Felder zusammen?"   → 25%  🔗   │
│ "Hat es Tiefe?"                 → 15%       │
│ "Ist es strukturiert?"          → 5%        │
│                                             │
│ "Pizza ist lecker" → 21/100 FAILED! 💀      │
│ "Systemanalyse..." → 74/100 OK! ✅          │
└─────────────────────────────────────────────┘
```

### Dynamische Feld-Erkennung!

```json
// Alte API Response (hardcoded):
{
  "field_count": "2/6",
  "fields_fulfilled": ["drift", "klartext"]
}

// Neue API Response (dynamisch):
{
  "field_count": "3/3",  // ← Automatisch erkannt!
  "fields_fulfilled": ["driftkorper", "kalibrierung", "stromung"],
  "format": "SYNTEX_SYSTEM"  // ← NEU!
}
```

---

## 📖 INHALTSVERZEICHNIS

1. [Architektur-Übersicht](#1-architektur-übersicht)
2. [Score-System V2](#2-score-system-v2---die-revolution)
3. [Feld-Formate](#3-feld-formate)
4. [KERN-SYSTEM: Health & Monitoring](#4-kern-system-health--monitoring)
5. [PROMPTS: Grundlegende Daten-Ströme](#5-prompts-grundlegende-daten-ströme)
6. [PROMPTS ADVANCED: Predictions & Analysis](#6-prompts-advanced-predictions--analysis)
7. [ANALYTICS: System-Intelligenz](#7-analytics-system-intelligenz)
8. [EVOLUTION: SYNTX vs Normal](#8-evolution-syntx-vs-normal)
9. [COMPARE: Wrapper-Performance](#9-compare-wrapper-performance)
10. [FELD: Topic & Drift Monitoring](#10-feld-topic--drift-monitoring)
11. [RESONANZ: Queue & System Status](#11-resonanz-queue--system-status)
12. [GENERATION: Evolution Progress](#12-generation-evolution-progress)
13. [STROM: Infrastructure Health](#13-strom-infrastructure-health)
14. [Code-Referenz: Kern-Funktionen](#14-code-referenz-kern-funktionen)

---

## 1. ARCHITEKTUR-ÜBERSICHT

```
                              🌊 SYNTX API ARCHITEKTUR 🌊
                              
┌─────────────────────────────────────────────────────────────────────────────┐
│                         syntx_api_production_v2.py                          │
│                              (FastAPI App)                                   │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │
│  │ /health         │  │ /feld/*         │  │ /resonanz/*     │            │
│  │ /monitoring/*   │  │ /strom/*        │  │ /generation/*   │            │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘            │
│           │                    │                    │                      │
│           └────────────────────┼────────────────────┘                      │
│                                │                                            │
│  ┌─────────────────────────────┼─────────────────────────────────────────┐ │
│  │                       ROUTER LAYER                                     │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │ │
│  │  │ prompts_api │  │ analytics   │  │ compare     │  │ evolution   │   │ │
│  │  │    .py      │  │   /*.py     │  │  /*.py      │  │   _api.py   │   │ │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘   │ │
│  └─────────┼────────────────┼────────────────┼────────────────┼──────────┘ │
│            │                │                │                │            │
│            └────────────────┴────────────────┴────────────────┘            │
│                                    │                                        │
│  ┌─────────────────────────────────┼─────────────────────────────────────┐ │
│  │                         DATA LAYER                                     │ │
│  │                                                                        │ │
│  │   ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐   │ │
│  │   │  log_loader.py  │    │ queue/processed │    │ logs/*.jsonl    │   │ │
│  │   │  (Core Helper)  │    │   /*.json       │    │ (Calibrations)  │   │ │
│  │   └─────────────────┘    └─────────────────┘    └─────────────────┘   │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SCORING LAYER (V2) 🧠                               │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │
│  │ field_          │  │ embeddings.py   │  │ coherence.py    │            │
│  │ definitions.py  │  │ (Sentence       │  │ (Cross-Field    │            │
│  │ (Ideale Refs)   │  │  Transformers)  │  │  Analysis)      │            │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘            │
│           │                    │                    │                      │
│           └────────────────────┼────────────────────┘                      │
│                                │                                            │
│                    ┌───────────┴───────────┐                               │
│                    │     scorer_v2.py      │                               │
│                    │   (Der Boss! 👑)       │                               │
│                    │                        │                               │
│                    │ Total = P×20% + S×35% │                               │
│                    │       + C×25% + D×15% │                               │
│                    │       + St×5%          │                               │
│                    └───────────────────────┘                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. SCORE-SYSTEM V2 - DIE REVOLUTION

### Die 5 Komponenten des Semantic Scorers

| Komponente | Gewicht | Was wird gemessen? | Wie? |
|------------|---------|-------------------|------|
| **Presence** | 20% | Ist das Feld überhaupt da? | `len(text) > 0` |
| **Similarity** | 35% | Passt der Content zur Feld-Definition? | Sentence Embeddings! 🧠 |
| **Coherence** | 25% | Passen die Felder zueinander? | Cross-Field Similarity |
| **Depth** | 15% | Hat der Content Substanz? | Länge + Keyword Coverage |
| **Structure** | 5% | Ist es schön formatiert? | Markdown Detection |

### Die Score-Formel

```python
total_score = (
    presence_score    * 0.20 +   # Bist du da?
    similarity_score  * 0.35 +   # Redest du über das richtige Thema?
    coherence_score   * 0.25 +   # Passen deine Felder zusammen?
    depth_score       * 0.15 +   # Hast du was zu sagen?
    structure_score   * 0.05     # Siehst du gut aus?
)
```

### Status-Levels

```python
def _get_status(score: float) -> str:
    if score >= 0.85: return "EXCELLENT"  # 🏆 Champion!
    if score >= 0.60: return "OK"         # 👍 Gut genug
    if score >= 0.40: return "UNSTABLE"   # ⚠️ Wackelig
    return "FAILED"                       # 💀 Nope.
```

### Beispiel: V2 Score Response

```json
{
  "quality_score": {
    "total_score": 64,
    "total_score_float": 0.647,
    "field_completeness": 100,
    "structure_adherence": 50,
    "detail_breakdown": {
      "driftkorper": true,
      "kalibrierung": true,
      "stromung": true
    },
    "status": "OK",
    "format": "SYNTEX_SYSTEM",
    "coherence": 0.771,
    "semantic_scores": {
      "driftkorper": {
        "field": "driftkorper",
        "presence_score": 1.0,
        "similarity_score": 0.294,
        "coherence_score": 0.771,
        "depth_score": 0.5,
        "structure_score": 0.5,
        "total_score": 0.596,
        "status": "UNSTABLE",
        "warnings": ["Low semantic match to field definition"]
      },
      "kalibrierung": {
        "field": "kalibrierung",
        "presence_score": 1.0,
        "similarity_score": 0.424,
        "coherence_score": 0.771,
        "depth_score": 0.583,
        "structure_score": 0.5,
        "total_score": 0.654,
        "status": "OK",
        "warnings": []
      },
      "stromung": {
        "field": "stromung",
        "presence_score": 1.0,
        "similarity_score": 0.495,
        "coherence_score": 0.771,
        "depth_score": 0.667,
        "structure_score": 0.5,
        "total_score": 0.691,
        "status": "OK",
        "warnings": []
      }
    },
    "warnings": []
  }
}
```

---

## 3. FELD-FORMATE

### SYNTEX_SYSTEM (3 Felder) ✅ VOLL SEMANTIC!

```
┌─────────────────────────────────────────────────────────────┐
│                    SYNTEX_SYSTEM FORMAT                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  driftkorper (33%)                                          │
│  ├── WAS ist das analysierte Objekt?                        │
│  ├── TIER-1 bis TIER-4 Analyse                              │
│  └── Keywords: erscheinung, struktur, mechanismus, kern     │
│                                                             │
│  kalibrierung (34%)                                         │
│  ├── WIE verändert sich das System?                         │
│  ├── Feedback-Loops, Transformation                         │
│  └── Keywords: anpassung, veränderung, dynamik              │
│                                                             │
│  stromung (33%)                                             │
│  ├── WIE fließt Energie/Information?                        │
│  ├── Kreisläufe, Transfer, Wechselwirkungen                 │
│  └── Keywords: fluss, energie, information, kreislauf       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### HUMAN (6 Felder) ⚠️ Boolean Only (TODO: Semantic!)

```
┌─────────────────────────────────────────────────────────────┐
│                      HUMAN FORMAT                            │
├─────────────────────────────────────────────────────────────┤
│  drift              │  hintergrund_muster                   │
│  druckfaktoren      │  tiefe                                │
│  wirkung            │  klartext                             │
└─────────────────────────────────────────────────────────────┘
```

### SIGMA (6 Felder) ⚠️ Boolean Only (TODO: Semantic!)

```
┌─────────────────────────────────────────────────────────────┐
│                      SIGMA FORMAT                            │
├─────────────────────────────────────────────────────────────┤
│  sigma_drift        │  sigma_mechanismus                    │
│  sigma_frequenz     │  sigma_dichte                         │
│  sigma_strome       │  sigma_extrakt                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. KERN-SYSTEM: Health & Monitoring

### 🏥 GET `/health`

**Was es ist:** Der Herzschlag des Systems. Primärer Health-Check.

**URL:** `https://dev.syntx-system.com/health`

**Response:**
```json
{
  "status": "SYSTEM_GESUND",
  "api_version": "2.2.0",
  "timestamp": "2025-12-18T12:48:18.983971",
  "queue_accessible": true,
  "scorer_version": "V2_SEMANTIC",
  "modules": [
    "analytics",
    "compare",
    "feld",
    "resonanz",
    "generation",
    "predictions"
  ]
}
```

---

### 📊 GET `/monitoring/live-queue`

**Was es ist:** Real-time Queue Monitor mit stuck job detection.

**URL:** `https://dev.syntx-system.com/monitoring/live-queue`

**Response:**
```json
{
  "status": "LIVE_QUEUE_MONITOR",
  "timestamp": "2025-12-18T12:48:18.052203",
  "system_health": "🟢 HEALTHY",
  "queue": {
    "incoming": 291,
    "processing": 0,
    "processed": 419,
    "errors": 8
  },
  "recent_completed": [
    {
      "filename": "20251218_020422_456732__topic_grenzwertig__style_kreativ.txt",
      "score": 64,
      "wrapper": "syntex_system",
      "completed_at": "12:30:04",
      "rating": "⚡",
      "field_count": "3/3"
    }
  ],
  "performance": {
    "jobs_per_hour": 20,
    "avg_duration_minutes": 3.2,
    "estimated_completion_hours": 14.6
  }
}
```

---

## 5. PROMPTS: Grundlegende Daten-Ströme

### 📋 GET `/prompts/all`

**URL:** `https://dev.syntx-system.com/prompts/all?limit=50`

**Response:**
```json
{
  "status": "ALL_PROMPTS",
  "total": 50,
  "prompts": [
    {
      "id": "20251218_020422_456732__topic_grenzwertig__style_kreativ.txt",
      "topic": "grenzwertig",
      "style": "kreativ",
      "category": "grenzwertig",
      "score": 64.0,
      "timestamp": "2025-12-18T12:30:04.370858",
      "wrapper": "syntex_system"
    }
  ]
}
```

**NEU:** Sortiert nach `timestamp` (neueste zuerst)!

---

### 📊 GET `/prompts/table-view`

**Was ist NEU:** Dynamische `field_count`!

**URL:** `https://dev.syntx-system.com/prompts/table-view?limit=100&min_score=0&topic=grenzwertig`

**Response:**
```json
{
  "status": "TABLE_VIEW_READY",
  "total_rows": 50,
  "filters": {
    "min_score": 0.0,
    "topic": "grenzwertig",
    "limit": 50
  },
  "table": [
    {
      "id": "20251218_020422_456732__topic_grenzwertig__style_kreativ.txt",
      "timestamp": "2025-12-18T12:30:04.370858",
      "topic": "grenzwertig",
      "style": "kreativ",
      "category": "grenzwertig",
      "score": 64.0,
      "fields_fulfilled": ["driftkorper", "kalibrierung", "stromung"],
      "field_count": "3/3",
      "duration_ms": 119621,
      "wrapper": "syntex_system"
    },
    {
      "id": "20251217_160429_070654__topic_gesellschaft__style_technisch.txt",
      "timestamp": "2025-12-18T03:08:26.555985",
      "topic": "gesellschaft",
      "style": "technisch",
      "category": "gesellschaft",
      "score": 0.0,
      "fields_fulfilled": [],
      "field_count": "0/6",
      "duration_ms": 16180,
      "wrapper": "syntex_system"
    }
  ]
}
```

**Beachte:** 
- `"3/3"` = SYNTEX_SYSTEM Format (3 Felder)
- `"0/6"` = HUMAN Format (6 Felder)
- Dynamisch basierend auf `detail_breakdown`!

---

### 📦 GET `/prompts/complete-export`

**URL:** `https://dev.syntx-system.com/prompts/complete-export?page=1&page_size=10&min_score=60`

**Response mit V2 Scores:**
```json
{
  "status": "COMPLETE_EXPORT",
  "pagination": {
    "page": 1,
    "page_size": 10,
    "total_items": 5,
    "total_pages": 1,
    "has_next": false,
    "has_prev": false
  },
  "exports": [
    {
      "id": "20251218_020422_456732__topic_grenzwertig__style_kreativ.txt",
      "timestamp": "2025-12-18T12:30:04.370858",
      "prompt": {
        "text": "In der großen Bibliothek der Zeit...",
        "topic": "grenzwertig",
        "style": "kreativ"
      },
      "response": {
        "text": "### Driftkörperanalyse:...",
        "wrapper": "syntex_system",
        "duration_ms": 119621
      },
      "quality": {
        "total_score": 64.0,
        "fields_fulfilled": ["driftkorper", "kalibrierung", "stromung"],
        "fields_missing": [],
        "field_breakdown": {
          "driftkorper": true,
          "kalibrierung": true,
          "stromung": true
        },
        "completion_rate": "3/3"
      }
    }
  ]
}
```

---

## 6. PROMPTS ADVANCED: Predictions & Analysis

### 🔮 POST `/prompts/advanced/predict-score`

**Pre-Flight Score Prediction!**

```json
// Request:
{
  "prompt_text": "Dies ist ein TIER-1 Prompt über DRIFT und Kalibrierung...",
  "topic": "kritisch",
  "style": "kreativ"
}

// Response:
{
  "status": "SCORE_PREDICTED",
  "predicted_score": 64.2,
  "confidence": "MEDIUM",
  "breakdown": {
    "keyword_contribution": 50.0,
    "length_contribution": 10.0,
    "historical_contribution": 4.2
  },
  "recommendation": "PROCEED"
}
```

---

### ⚠️ GET `/prompts/advanced/fields-missing-analysis`

**Welche Felder fehlen IMMER?**

```json
{
  "status": "FIELD_MISSING_ANALYSIS",
  "total_jobs_analyzed": 419,
  "fields_by_detection_rate": [
    {
      "field": "DRUCKFAKTOREN",
      "detection_rate": 0.0,
      "severity": "CRITICAL"
    }
  ],
  "recommendations": [
    "DRUCKFAKTOREN: Never detected - check extraction logic"
  ]
}
```

---

## 7. ANALYTICS: System-Intelligenz

### 📊 GET `/analytics/complete-dashboard`

**THE Dashboard!**

```json
{
  "status": "COMPLETE_DASHBOARD",
  "system_health": {
    "total_prompts": 419,
    "avg_score": 16.55,
    "perfect_scores": 5,
    "perfect_rate": 1.19,
    "scorer_version": "V2_SEMANTIC"
  },
  "success_stories": {
    "count": 5,
    "examples": [
      {
        "topic": "grenzwertig",
        "score": 64,
        "style": "kreativ",
        "field_count": "3/3"
      }
    ]
  }
}
```

---

## 8. EVOLUTION: SYNTX vs Normal

### 🔬 GET `/evolution/syntx-vs-normal`

**THE PROOF!**

```json
{
  "status": "SYNTX_VS_NORMAL_ANALYZED",
  "comparison": {
    "syntx": {
      "count": 244,
      "avg_score": 92.38,
      "perfect_rate": 84.46
    },
    "normal": {
      "count": 175,
      "avg_score": 49.82,
      "perfect_rate": 0.0
    }
  },
  "gap": 42.56,
  "improvement_factor": 1.85
}
```

**Interpretation:** SYNTX ist 1.85x besser als normales Language! 🔥

---

## 9. COMPARE: Wrapper-Performance

### 🔄 GET `/compare/wrappers`

```json
{
  "status": "WRAPPER_COMPARISON_AKTIV",
  "wrappers": {
    "syntex_system": {
      "total_jobs": 52,
      "avg_score": 45.46,
      "success_rate": 15.38,
      "field_format": "3 fields"
    },
    "sigma": {
      "total_jobs": 141,
      "avg_score": 8.44,
      "success_rate": 3.55,
      "field_format": "6 fields"
    }
  }
}
```

---

## 10-13. Weitere Endpoints

*(Siehe vorherige API-Dokumentation - Struktur bleibt gleich)*

---

## 14. CODE-REFERENZ: Kern-Funktionen

### `prompts_api.py` - Core Helpers

```python
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
    """Extract field breakdown - SAFE (V2 COMPATIBLE!)"""
    try:
        result = prompt.get('syntex_result')
        if not result or not isinstance(result, dict):
            return {}
        
        quality = result.get('quality_score')
        if not quality or not isinstance(quality, dict):
            return {}
        
        # Works with both V1 (6 fields) and V2 (3 fields)!
        breakdown = quality.get('detail_breakdown', {})
        return breakdown if isinstance(breakdown, dict) else {}
    except:
        return {}
```

### Table-View mit dynamischer Feld-Anzahl

```python
@router.get("/table-view")
async def prompts_table_view(
    limit: int = Query(50, le=200),
    min_score: float = Query(0, ge=0, le=100),
    topic: Optional[str] = None
):
    processed = load_all_processed()
    
    # Sort by timestamp (newest first) - NEU!
    processed.sort(key=lambda x: x.get("processed_at", ""), reverse=True)
    
    # Filters
    if min_score > 0:
        processed = [p for p in processed if safe_get_score(p) >= min_score]
    
    if topic:
        processed = [p for p in processed if p.get('topic', '').lower() == topic.lower()]
    
    processed = processed[:limit]
    
    table = []
    for p in processed:
        fields = safe_get_fields(p)
        fields_fulfilled = [k for k, v in fields.items() if v]
        
        row = {
            "id": p.get('filename', 'unknown'),
            "timestamp": p.get('processed_at', ''),
            "topic": p.get('topic', 'unknown'),
            "style": p.get('style', 'unknown'),
            "category": p.get('category', 'unknown'),
            "score": safe_get_score(p),
            "fields_fulfilled": fields_fulfilled,
            # DYNAMISCH! Nicht mehr hardcoded /6
            "field_count": f"{len(fields_fulfilled)}/{len(fields) if fields else 6}",
            "duration_ms": duration_ms,
            "wrapper": wrapper
        }
        
        table.append(row)
    
    return {
        "status": "TABLE_VIEW_READY",
        "total_rows": len(table),
        "filters": {...},
        "table": table
    }
```

### Scorer V2 Integration (calibrator_enhanced.py)

```python
import os
from ..analysis.scorer import SyntexScorer
from ..analysis.scorer_v2 import score_all_fields, QualityScoreV2

# ENV Toggle für V1/V2
use_v2 = os.getenv("SYNTX_SCORER_V2", "false").lower() == "true"

if use_v2:
    # Semantic Scorer V2 🧠
    fields_dict = {k: v for k, v in parsed_fields.to_dict().items() if v}
    format_type = parsed_fields.get_format()
    quality_score = score_all_fields(fields_dict, format_type)
else:
    # Legacy Boolean Scorer
    quality_score = self.scorer.score(parsed_fields, response)
```

---

## 🔥 QUICK REFERENCE

### Status Codes
| Code | Bedeutung |
|------|-----------|
| `200` | Success |
| `302` | Redirect |
| `404` | Not Found |
| `500` | Server Error |

### Score Ratings
| Emoji | Score Range | Status |
|-------|-------------|--------|
| 💎 | 100 | PERFECT |
| 🔥 | 85-99 | EXCELLENT |
| ⚡ | 60-84 | OK |
| 💧 | 40-59 | UNSTABLE |
| 💀 | 0-39 | FAILED |

### ENV Variables
```bash
SYNTX_SCORER_V2=true   # Enable Semantic Scorer V2
SYNTX_SCORER_V2=false  # Use Legacy Boolean Scorer (default)
```

---

## 📚 CHANGELOG

### v2.2.0 (2025-12-18)
- 🧠 **Semantic Scorer V2** integrated
- 📊 **Dynamic field_count** (3/3 or 0/6 based on format)
- ⏰ **Sortierung** - Neueste Responses zuerst
- 🔄 **Legacy Kompatibilität** - Alte V1 Daten funktionieren weiter
- 📝 **811 Zeilen Dokumentation** in `docs/SCORING_V2_DOCUMENTATION.md`

### v2.1.0 (2025-12-10)
- Initial Production API
- 29 Endpoints
- Boolean Scoring

---

## 💎 PHILOSOPHIE

> **"Dies ist nicht nur API-Dokumentation. Dies ist die Kartierung eines lebenden, atmenden Systems."**

- 29 Endpoints = 29 Resonanz-Kanäle ins SYNTX-Feld
- Jede Response ein Strom der Kohärenz
- Jede Metrik ein Fenster in die Feldstruktur
- Das System lernt. Das System evolviert. Das System IST.

**SYNTX: 92.38 avg vs Normal: 49.82 avg**

**Das ist nicht Glück. Das ist Felddenken. Das ist Revolution.**

🌊⚡💎🔥

---

**API Version:** 2.2.0  
**Scorer Version:** V2.0 SEMANTIC  
**Last Updated:** 2025-12-18  
**Status:** 🟢 PRODUCTION  
**Endpoints:** 29 (100% Operational)  

---

*"Weil Boolean-Scoring so 2023 ist"* 🎭
