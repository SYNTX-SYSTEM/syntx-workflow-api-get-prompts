# 🌊 STROM CRUD - First-Class Calibration Streams

## SYNTX Charlottenburg Terminologie

**Das Problem war klar:** Ströme waren implizit. Crons existierten de facto, aber nicht als First-Class-Objekte. Keine Definition. Keine Ownership. Keine saubere Architektur.

**Die Lösung:** Ströme werden zu echten Entitäten. Mit CRUD. Mit Storage. Mit Architektur.

---

## 🔥 Die Architektur-Entscheidung

### Warum STROM als First-Class Entity?

Claude hat einen harten Befund geliefert:
- `generator.yaml` hatte keine explizite `crons:` Section
- Crons existierten implizit, nicht als definierte Objekte
- UPDATE ohne CREATE ist architektonisch falsch
- DELETE ohne Ownership ist gefährlich

**Die Konsequenz:** Wir machen Ströme zu echten Objekten.

### SYNTX::STROM Definition

Ein Strom ist:
- **zeitlich steuerbar** (Cron-Pattern)
- **modellgebunden** (GPT-4, etc.)
- **feldkalibriert** (Topic-Gewichte)
- **reproduzierbar** (Persistente Definition)
- **visuell darstellbar** (Für CALIBRAX UI)
- **auditierbar** (Created/Updated Timestamps)

---

## 💎 Storage-Architektur

### Drei Ebenen
```
EBENE 1: DEFINITION
/opt/syntx-config/stroeme/stroeme.yaml
→ Was soll laufen

EBENE 2: EXECUTION  
/opt/syntx-config/queue/incoming/*.json
→ Was läuft jetzt

EBENE 3: RESULTATE
/opt/syntx-config/generator-data/syntex_calibrations.jsonl
→ Was ist passiert
```

**Saubere Trennung. Keine Vermischung. Architektonisch korrekt.**

---

## ⚡ Die 5 CRUD Operations

### 1️⃣ CREATE - POST /strom/crud

**Zweck:** Neuen Kalibrierungs-Strom definieren und persistent machen.

**Endpoint:** `POST https://dev.syntx-system.com/api/strom/crud`

**Request Body:**
```json
{
  "name": "Evening Analysis Flow",
  "zeitplan": "0 18 * * *",
  "modell": "gpt-4o",
  "felder_topics": {
    "bildung": 0.8,
    "technologie": 0.6
  },
  "styles": ["technisch", "akademisch"],
  "sprachen": ["de", "en"],
  "aktiv": true
}
```

**Response:**
```json
{
  "strom_id": "strom_b99caf3e",
  "muster": "evening_analysis_flow",
  "name": "Evening Analysis Flow",
  "zeitplan": "0 18 * * *",
  "modell": "gpt-4o",
  "felder_topics": {
    "bildung": 0.8,
    "technologie": 0.6
  },
  "styles": ["technisch", "akademisch"],
  "sprachen": ["de", "en"],
  "aktiv": true,
  "created_at": "2026-01-08T16:11:14.507533",
  "updated_at": "2026-01-08T16:11:14.507533"
}
```

**Was passiert:**
- Generiert `strom_id` (UUID-basiert)
- Generiert `muster` aus Name (lowercase, underscores)
- Prüft auf Duplikate
- Speichert in `stroeme.yaml`

---

### 2️⃣ READ ALL - GET /strom/crud

**Zweck:** Alle existierenden Ströme abrufen. Grundlage für UI, Timeline, 3D-Visualisierung.

**Endpoint:** `GET https://dev.syntx-system.com/api/strom/crud`

**Query Params:**
- `aktiv_only` (bool): Nur aktive Ströme zurückgeben

**Response:**
```json
[
  {
    "strom_id": "strom_001",
    "muster": "example_morning_strom",
    "name": "Morning Calibration Flow",
    "zeitplan": "0 8 * * 1-5",
    "modell": "gpt-4o",
    "felder_topics": {
      "systemstruktur": 0.9,
      "humansprache": 0.6
    },
    "styles": ["technisch", "akademisch"],
    "sprachen": ["de", "en"],
    "aktiv": true,
    "created_at": "2026-01-08T16:00:00Z",
    "updated_at": "2026-01-08T16:00:00Z"
  }
]
```

---

### 3️⃣ READ SINGLE - GET /strom/crud/{muster}

**Zweck:** Einzelnen Strom abrufen.

**Endpoint:** `GET https://dev.syntx-system.com/api/strom/crud/example_morning_strom`

**Response:** Wie READ ALL, aber einzelnes Objekt statt Array.

---

### 4️⃣ UPDATE - PUT /strom/crud/{muster}

**Zweck:** Bestehenden Strom modifizieren.

**Endpoint:** `PUT https://dev.syntx-system.com/api/strom/crud/evening_analysis_flow`

**Request Body (partial):**
```json
{
  "zeitplan": "0 20 * * *",
  "felder_topics": {
    "bildung": 0.9
  }
}
```

**Response:** Komplettes Strom-Objekt mit aktualisiertem `updated_at`.

**Was kann geändert werden:**
- `name` - Anzeigename
- `zeitplan` - Cron-Expression
- `modell` - AI-Modell
- `felder_topics` - Field-Gewichte
- `styles` - Style-Präferenzen
- `sprachen` - Sprachen
- `aktiv` - Aktivierungsstatus

---

### 5️⃣ DELETE - DELETE /strom/crud/{muster}

**Zweck:** Strom-Definition entfernen (Logs bleiben erhalten).

**Endpoint:** `DELETE https://dev.syntx-system.com/api/strom/crud/test_evening_flow`

**Response:**
```json
{
  "erfolg": true,
  "status": "gelöscht",
  "muster": "test_evening_flow",
  "strom_id": "strom_b99caf3e"
}
```

**Wichtig:** DELETE entfernt nur die Definition. Execution-Logs in `syntex_calibrations.jsonl` bleiben erhalten für Audit-Trail.

---

## 🧠 SYNTX Terminologie im Code

### Deutsch → Englisch Mapping

- **strom** = calibration stream/flow
- **feld** = semantic field
- **kalibrierung** = calibration
- **muster** = pattern identifier
- **zeitplan** = schedule (cron expression)
- **felder_topics** = field topic weights
- **aktiv** = active status

### Warum Deutsch?

**SYNTX ist Deutsch.** Die Core-Konzepte (Drift, Feld, Resonanz, Strom) sind Deutsche Begriffe. Das API reflektiert das. Authentisch. Unverfälscht. Nicht übersetzt.

---

## 🔧 Technische Implementation

### Router

**File:** `api-core/strom_crud_router.py`

**Prefix:** `/strom/crud`

**Tags:** `["strom-crud"]`

**Storage:** `/opt/syntx-config/stroeme/stroeme.yaml`

### Pydantic Models
```python
class StromCreate(BaseModel):
    name: str
    zeitplan: str  # Cron pattern
    modell: str = "gpt-4o"
    felder_topics: Dict[str, float] = {}
    styles: List[str] = ["technisch"]
    sprachen: List[str] = ["de"]
    aktiv: bool = True

class StromUpdate(BaseModel):
    # All fields optional
    name: Optional[str] = None
    zeitplan: Optional[str] = None
    modell: Optional[str] = None
    felder_topics: Optional[Dict[str, float]] = None
    styles: Optional[List[str]] = None
    sprachen: Optional[List[str]] = None
    aktiv: Optional[bool] = None

class StromResponse(BaseModel):
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
```

---

## 🌊 Integration in Main API

**File:** `api-core/syntx_api_production_v2.py`
```python
from strom_crud_router import router as strom_crud_router

app.include_router(strom_crud_router)
```

**Nginx Config:** `/etc/nginx/sites-available/dev.syntx-system.com`
```nginx
location /api/strom/crud {
    proxy_pass http://127.0.0.1:8020/strom/crud;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

---

## ✅ Testing

### All 5 Operations Tested
```bash
bash scripts/all_api_calls.sh
```

**Results:**
- ✅ GET /strom/crud - List All (200 OK)
- ✅ GET /strom/crud/{muster} - Get Single (200 OK)
- ✅ POST /strom/crud - Create (200 OK)
- ✅ PUT /strom/crud/{muster} - Update (200 OK)
- ✅ DELETE /strom/crud/{muster} - Delete (200 OK)

**Pass Rate:** 100% (5/5)

---

## 🎯 Next Steps - Phase 2

Mit STROM CRUD als Foundation können wir jetzt bauen:

1. **GPT Input CRUD** - Manage Meta-Prompts
2. **Strom → GPT Zuordnung** - Welcher Input für welchen Strom
3. **Execution Layer** - Ströme aktivieren/triggern
4. **CALIBRAX UI** - Visuelle Strom-Kontrolle
5. **Grade System** - Strom-Grade vs Input-Grade

---

## 💎 Warum das revolutionär ist

**Vorher:**
- Crons existierten implizit
- Keine Definition
- Keine Kontrolle
- Keine Visualisierung

**Jetzt:**
- Ströme sind First-Class Entities
- Vollständiges CRUD
- Persistente Storage
- API-gesteuert
- UI-ready

**Das ist nicht nur ein Feature. Das ist Architektur.**

---

## 🔥 Die Essenz

Ein Strom ist nicht einfach ein Cronjob. Ein Strom ist:

**Eine zeitlich definierte, modellgebundene, feldkalibrierte, reproduzierbare Kalibrierungs-Einheit, die als First-Class-Objekt im System existiert, visuell darstellbar ist, und durch vollständiges CRUD kontrollierbar wird.**

**Das ist SYNTX.**

---

💎⚡🔥🌊👑

**STROM CRUD - PHASE 1A COMPLETE**

2026-01-08 | Andi & Claude | Charlottenburg Architektur
