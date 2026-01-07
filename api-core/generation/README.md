# 🌊 SYNTX STROM-ORCHESTRATOR API - NEUKÖLLN EDITION

**Yo, pass auf Bruder!** 💎⚡ **JETZT KOMMT DIE ULTIMATIVE DOKU! NEUKÖLLNER STRASSENSLANG TRIFFT SYNTX-TERMINOLOGIE!** 🔥🌊

Dies ist nicht irgendeine API. Dies ist der **STROM-ORCHESTRATOR** – das Herzstück für die Kalibrierung und Steuerung des kompletten SYNTX Prompt-Generation-Systems.

**Was du hier findest:**
- **🔥 KRONTUN** - 3 Endpoints für Real Calibration Data (1288 echte Production Runs!)
- **⚖️ TOPIC WEIGHTS** - 4 Endpoints für persistente Priority Control
- **💎 FELD-BASIERTE ARCHITEKTUR** - Keine Token-Scheiße, nur Ströme und Resonanz
- **🌊 PURE LINUX STACK** - Kein Docker-Overhead, nur raw systemd power
- **👑 SYNTX-TERMINOLOGIE** durchgehend - Drift, Kohärenz, Resonanz, Felder

**Kein Blabla. Nur Felder. Nur Ströme. Nur Resonanz.**

---

## 📍 WO LÄUFT DER SCHEISS?

**Lokal (Dev):**
- `http://127.0.0.1:8020`
- FastAPI Auto-Docs: `http://127.0.0.1:8020/docs`

**Production (Live Alter!):**
- `https://dev.syntx-system.com/api/strom/`
- Nginx Proxy → Port 8020
- SSL via Let's Encrypt
- **100% PASS RATE** auf allen 36 Endpoints

**Service Management:**
```bash
# Status checken
sudo systemctl status syntx-api.service

# Neustarten (wenn du Scheiße gebaut hast)
sudo systemctl restart syntx-api.service

# Logs live (see the magic happen)
sudo journalctl -u syntx-api.service -f
```

---

## 🗂️ FILE STRUKTUR - WO IST WAS BRUDER?
```
/opt/syntx-workflow-api-get-prompts/
├── api-core/
│   ├── generation/
│   │   ├── generation_api.py          # Topic Weights (4 Endpoints)
│   │   ├── topic_weights_handler.py   # Persistent Storage Logic
│   │   └── README.md                  # Diese geile Datei hier! 🔥
│   ├── kalibrierung_router.py         # 🆕 KRONTUN (3 Endpoints)
│   ├── syntx_api_production_v2.py     # Main API (36 Endpoints Total)
│   └── [analytics, formats, prompts, monitoring...]
├── configs/
│   └── generator.yaml                 # Runtime Config
└── /opt/syntx-config/
    ├── configs/
    │   └── topic_weights.json         # Persistent Topic Weights
    └── generator-data/
        └── syntex_calibrations.jsonl  # 🔥 1288 ECHTE CALIBRATIONS!
```

---

## 🎯 ALLE ENDPOINTS - KOMPLETTER ÜBERBLICK

### **🌀 KRONTUN - REAL CALIBRATION DATA** (3 Endpoints)

**Das ist der neue Shit Bruder!** Real Production Data aus `syntex_calibrations.jsonl` - 1288 echte Calibration Runs mit Quality Scores, Drift, Duration, alles!

#### `GET /kalibrierung/cron/stats`
**Was:** Live Stats - wie viele Calibrations liefen, wie viele failed

**Response:**
```json
{
  "erfolg": true,
  "active": 0,
  "pending": 0,
  "completed": 1281,
  "failed": 7,
  "total": 1288
}
```

**Use Case:** Dashboard - zeig mir die Zahlen Alter! 99.5% Success Rate! 🔥

---

#### `GET /kalibrierung/cron/logs?limit=5`
**Was:** Echte Calibration History mit Quality Scores und Drift

**Response:**
```json
{
  "erfolg": true,
  "anzahl": 5,
  "logs": [
    {
      "cron_id": "calibration-2025-12-18T10:32:56",
      "timestamp": "2025-12-18T10:32:56.449517Z",
      "cron_data": {
        "name": "SYNTEX::TRUE_RAW Calibration",
        "modell": "mistral-uncensored",
        "anzahl": 1,
        "felder": {
          "Driftkorper": 1.0,
          "Kalibrierung": 1.0,
          "Stromung": 1.0
        }
      },
      "result": {
        "status": "completed",
        "generated": 1,
        "failed": 0,
        "avg_quality": 100,
        "drift": 0.05,
        "cost": 0.01,
        "duration_ms": 151734
      }
    }
  ]
}
```

**SYNTX Felder Explained:**
- **Driftkorper** - WAS wird analysiert (Substanz, Struktur, Kern)
- **Kalibrierung** - WIE wird optimiert (Präzision, Resonanz)
- **Stromung** - WIE fließt es (Bewegung, Energie, Richtung)

**Use Case:** Timeline - zeig mir die letzten Runs, was lief gut, was failed?

---

#### `GET /kalibrierung/cron/impact`
**Was:** Impact Analytics - Topics x Time Heatmap (Placeholder für jetzt)

**Response:**
```json
{
  "erfolg": true,
  "impact": []
}
```

**Use Case:** Future - zeige welche Topics wann am meisten processed wurden.

---

### **⚖️ TOPIC WEIGHTS - PERSISTENT PRIORITY CONTROL** (4 Endpoints)

**Persistent Topic Gewichtungen!** Speichert in `/opt/syntx-config/configs/topic_weights.json` - überlebt Server-Restart, keine Session-Scheiße!

#### `GET /topic-weights`
**Was:** Alle gespeicherten Topic-Gewichtungen holen

**Response:**
```json
{
  "erfolg": true,
  "weights": {
    "Quantencomputer": 0.85,
    "KI": 0.92,
    "Blockchain": 0.65
  },
  "anzahl": 3
}
```

**Use Case:** Frontend lädt beim Start die gespeicherten Gewichtungen - User sieht sofort seine Priorities!

---

#### `PUT /topic-weights`
**Was:** ALLE Topic-Gewichtungen auf einmal speichern (Bulk Update Bruder!)

**Request:**
```json
{
  "weights": {
    "Quantencomputer": 0.85,
    "Künstliche Intelligenz": 0.92,
    "Blockchain 2.0": 0.65,
    "Kochen und Rezepte": 0.20
  }
}
```

**Validation:**
- Weight muss `0.0 - 1.0` sein (sonst gibts Error Alter!)
- Weights außerhalb Range → 400 Bad Request

**Response:**
```json
{
  "erfolg": true,
  "gespeichert": 4,
  "message": "✅ 4 Topic-Gewichtungen gespeichert"
}
```

**Use Case:** User hat Bubbles im Frontend verschoben, alle Weights auf einmal speichern - ATOMIC!

---

#### `GET /topic-weights/{topic_name}`
**Was:** Gewichtung für EIN einzelnes Topic holen

**Example:**
```bash
curl https://dev.syntx-system.com/api/strom/topic-weights/Quantencomputer
```

**Response:**
```json
{
  "erfolg": true,
  "topic": "Quantencomputer",
  "weight": 0.85
}
```

**Use Case:** Check Weight für spezifisches Topic - "Wie wichtig ist mir Quantencomputer gerade?"

---

#### `PUT /topic-weights/{topic_name}`
**Was:** Gewichtung für EIN Topic updaten (Single Update Bruder!)

**Request:**
```bash
curl -X PUT https://dev.syntx-system.com/api/strom/topic-weights/Quantencomputer \
  -H "Content-Type: application/json" \
  -d '{"weight": 0.95}'
```

**Response:**
```json
{
  "erfolg": true,
  "topic": "Quantencomputer",
  "weight": 0.95,
  "message": "✅ Gewichtung für Quantencomputer auf 0.95 gesetzt"
}
```

**Use Case:** User clickt auf eine Bubble → Weight +10% - sofort gespeichert!

---

## 🗄️ STORAGE - WO LANDET DER SCHEISS?

### 🔥 Calibration Data (Read-Only)

**File:** `/opt/syntx-config/generator-data/syntex_calibrations.jsonl`

**1288 Zeilen echter Production Data!**
```json
{
  "timestamp": "2025-11-28T10:20:52.865314Z",
  "system": "SYNTEX::TRUE_RAW",
  "meta_prompt": "Erstelle eine Vision für...",
  "success": true,
  "duration_ms": 59451,
  "quality_score": {
    "total_score": 98,
    "field_completeness": 100,
    "structure_adherence": 96,
    "detail_breakdown": {
      "drift": true,
      "hintergrund_muster": true,
      "druckfaktoren": true,
      "tiefe": true,
      "wirkung": true,
      "klartext": true
    }
  },
  "parsed_fields": {
    "drift": "...",
    "hintergrund_muster": "...",
    "druckfaktoren": "...",
    "tiefe": "...",
    "wirkung": "...",
    "klartext": "..."
  }
}
```

**Eigenschaften:**
- **Read-Only:** API liest nur, schreibt nicht
- **1288 Calibrations:** Echte Production Runs
- **99.5% Success Rate:** 1281 completed, 7 failed
- **SYNTX Fields:** drift, hintergrund_muster, druckfaktoren, tiefe, wirkung, klartext

---

### ⚖️ Topic Weights Storage (Read-Write)

**File:** `/opt/syntx-config/configs/topic_weights.json`
```json
{
  "weights": {
    "Quantencomputer": 0.85,
    "Künstliche Intelligenz": 0.92,
    "Blockchain 2.0": 0.65
  },
  "last_updated": "2026-01-07T18:30:45.123456",
  "total_topics": 3
}
```

**Eigenschaften:**
- **Persistent:** Überlebt Server-Restart
- **Atomic Writes:** Keine Race Conditions (file lock baby!)
- **Default Weight:** 0.5 für neue Topics
- **Validation:** 0.0 - 1.0 Range enforced (sonst gibts Error!)

---

## 🎬 USE CASE FLOWS - SO NUTZT DU DEN SCHEISS!

### Flow 1: Topic Weights setzen → Frontend zeigt gespeicherte Priorities
```bash
# 1. Alle Weights holen (Frontend Init)
curl https://dev.syntx-system.com/api/strom/topic-weights

# 2. User verschiebt Bubbles im Frontend
# Frontend sendet: Alle neuen Weights auf einmal

curl -X PUT https://dev.syntx-system.com/api/strom/topic-weights \
  -H "Content-Type: application/json" \
  -d '{
    "weights": {
      "Quantencomputer": 0.9,
      "Künstliche Intelligenz": 0.8,
      "Blockchain 2.0": 0.3
    }
  }'

# 3. Server speichert persistent
# 4. User refresht Browser → Bubbles bleiben wo sie waren! 🔥
```

**Resultat:** Keine Session-Scheiße mehr! Weights überleben Browser Refresh, Server Restart, alles!

---

### Flow 2: KRONTUN Dashboard - Real Production Stats
```bash
# 1. Stats laden
curl https://dev.syntx-system.com/api/strom/kalibrierung/cron/stats

# Response: 1281 completed, 7 failed, 1288 total
# Frontend zeigt: 99.5% Success Rate!

# 2. Recent Executions laden
curl https://dev.syntx-system.com/api/strom/kalibrierung/cron/logs?limit=10

# Response: Letzte 10 Calibrations mit Quality Scores, Drift, Duration

# 3. User clickt auf Calibration → Modal öffnet
# Frontend zeigt:
# - Quality Score: 100
# - Drift: 0.05 (5%)
# - Duration: 151s
# - Fields: Driftkorper, Kalibrierung, Stromung
# - Status: completed ✅
```

**Resultat:** Live Dashboard mit echten Production Daten! Keine Mocks! Nur echte Ströme! 🌊

---

### Flow 3: Single Topic Weight updaten
```bash
# User clickt auf "Quantencomputer" Bubble
# Frontend sendet: +10% Weight

curl -X PUT https://dev.syntx-system.com/api/strom/topic-weights/Quantencomputer \
  -H "Content-Type: application/json" \
  -d '{"weight": 0.95}'

# Server speichert sofort
# Response: "✅ Gewichtung für Quantencomputer auf 0.95 gesetzt"
# Frontend updated Bubble Position live!
```

**Resultat:** Instant Update, keine Verzögerung, sofort persistent!

---

## 🔧 TECH STACK - WOMIT LÄUFT DER SCHEISS?

**Backend:**
- Python 3.12
- FastAPI (für die Endpoints Bruder!)
- Pydantic (Validation - keine Bad Requests!)
- JSON (Topic Weights Storage - simpel, robust)

**Infrastructure:**
- Systemd (Service Management - kein Docker-Overhead!)
- Nginx (Reverse Proxy - SSL Termination)
- Let's Encrypt (SSL - Gratis aber geil!)

**File System:**
- `/opt/syntx-workflow-api-get-prompts/` - Code
- `/opt/syntx-config/` - Config + Data

---

## 🐛 TROUBLESHOOTING - WENN SCHEISSE PASSIERT

### Problem: "Weights werden nicht gespeichert"

**Check das Bruder:**
```bash
# 1. Service läuft?
sudo systemctl status syntx-api.service

# 2. File writable?
ls -la /opt/syntx-config/configs/topic_weights.json

# 3. Permissions OK?
sudo chown syntx-api:syntx-api /opt/syntx-config/configs/topic_weights.json

# 4. Logs checken
sudo journalctl -u syntx-api.service -f
```

**Solution:** Fix Permissions oder restart Service!

---

### Problem: "API gibt 404"

**Check das Bruder:**
```bash
# 1. Nginx Config OK?
sudo nginx -t

# 2. Direct API call OK?
curl http://127.0.0.1:8020/kalibrierung/cron/stats

# 3. Via Nginx OK?
curl https://dev.syntx-system.com/api/strom/kalibrierung/cron/stats

# 4. Endpoint richtig?
# Richtig: /kalibrierung/cron/stats
# Falsch:  /calibration/cron/stats  (keine englische Scheiße!)
```

**Solution:** Check Nginx Proxy Config oder restart Service!

---

### Problem: "Calibration Data nicht aktuell"

**Check das Bruder:**
```bash
# 1. File existiert?
ls -la /opt/syntx-config/generator-data/syntex_calibrations.jsonl

# 2. Wie viele Zeilen?
wc -l /opt/syntx-config/generator-data/syntex_calibrations.jsonl

# 3. Neueste Timestamp?
tail -1 /opt/syntx-config/generator-data/syntex_calibrations.jsonl | jq '.timestamp'

# 4. API liest richtig?
curl https://dev.syntx-system.com/api/strom/kalibrierung/cron/logs?limit=1 | jq '.logs[0].timestamp'
```

**Solution:** File ist read-only für API - wird von anderem Service geschrieben!

---

## 💎 SYNTX TERMINOLOGIE - LERN DEN SCHEISS!

### 🌊 **STROM**
**Was:** Nicht "Daten", nicht "Requests" - **STROM** ist der Fluss der Felder durch das System.

**Beispiel:**
- Token-Denken: "Ich schicke einen Request zur API"
- Feld-Denken: "Ich initiiere einen STROM durch die Resonanzfelder"

---

### 💎 **FELD**
**Was:** Nicht "Kategorie", nicht "Tag" - **FELD** ist ein semantischer Resonanzraum.

**Beispiel:**
- Topics sind Felder: "Quantencomputer", "KI", "Blockchain"
- Nicht "Themen" - FELDER! Weil sie resonieren!

---

### ⚡ **KOHÄRENZ**
**Was:** Nicht "Quality", nicht "Correctness" - **KOHÄRENZ** ist die Übereinstimmung der Resonanzfelder.

**Beispiel:**
- Quality Score 100 = Maximale Kohärenz
- Quality Score 50 = Drift (Feld-Verlust)
- Quality Score 0 = Komplette Dekohärenz (Failed)

---

### 🔥 **DRIFT**
**Was:** Nicht "Error", nicht "Bug" - **DRIFT** ist Feld-Verlust, Resonanz-Abweichung.

**Beispiel:**
- Drift 0.05 (5%) = Minimaler Feld-Verlust
- Drift 0.40 (40%) = Hoher Feld-Verlust
- Drift > 0.20 = Warning Territory!

---

### 🌊 **KALIBRIERUNG**
**Was:** Nicht "Training", nicht "Optimization" - **KALIBRIERUNG** ist Resonanz-Justierung.

**Beispiel:**
- 1288 Calibrations = 1288 Resonanz-Justierungen
- Jede Calibration optimiert die Feld-Parameter
- Nicht "Training Runs" - KALIBRIERUNGEN!

---

### 👑 **RESONANZ**
**Was:** Nicht "Response", nicht "Output" - **RESONANZ** ist die Antwort des Feldes.

**Beispiel:**
- Token-Denken: "Das Modell gibt eine Response zurück"
- Feld-Denken: "Das Feld erzeugt eine RESONANZ"

---

## 🔥 SYNTX PHILOSOPHIE - WARUM DER SCHEISS WICHTIG IST

**Das ist nicht "noch eine API". Das ist Feld-Steuerung.**

### Alt (Token-Denken):
```
User → Schickt Request
API → Processed Request
System → Generiert Token
User → Bekommt Response
User → Vergisst alles
User → Nächstes Mal wieder von vorne
```

**Problem:** Keine Persistenz, keine Prioritäten, keine Resonanz!

---

### Neu (Feld-Denken):
```
User → Kalibriert Felder (Topic Weights)
System → Speichert Resonanz-Parameter (persistent!)
User → Initiiert Strom
System → Weiß automatisch: Welche Felder stark resonieren
System → Generiert Kohärente Ströme
User → Nie wieder manuelle Kalibrierung
User → System kennt seine Priorities!
```

**Lösung:** Persistente Resonanz, automatische Kohärenz, lückenloser Strom!

---

## 📊 CURRENT STATUS - WO STEHEN WIR?

**Live System:**
- ✅ **7 Endpoints aktiv** (3 KRONTUN + 4 Topic Weights)
- ✅ **1288 echte Calibrations** aus Production
- ✅ **99.5% Success Rate** (1281 completed, 7 failed)
- ✅ **Persistent Weights** überleben Server-Restart
- ✅ **API Latency ~78ms** (Avg Response Time)
- ✅ **SSL aktiv** (Let's Encrypt)
- ✅ **Service stabil** (Systemd managed)
- ✅ **100% Test Pass Rate** (36/36 Endpoints)

**Production Metrics:**
- **Total API Endpoints:** 36 (across all routers)
- **KRONTUN Endpoints:** 3 (Real Calibration Data)
- **Topic Weights Endpoints:** 4 (Persistent Storage)
- **Analytics Endpoints:** 7
- **Formats Endpoints:** 9
- **Prompts Endpoints:** 4
- **Monitoring Endpoints:** 1
- **Evolution Endpoints:** 2
- **Feld & Strom Endpoints:** 4
- **Health Endpoints:** 2

---

## 🎯 ROADMAP - WAS KOMMT NOCH?

### Phase 1: ✅ DONE
- KRONTUN Backend (3 Endpoints)
- Real Calibration Data (1288 Runs)
- Topic Weights Persistence (4 Endpoints)
- Frontend Integration (Live Dashboard)

### Phase 2: 🔥 IN PROGRESS
- **CALIBRAX** - 3D Timeline Visualization
  - Plot Calibrations in 3D Space
  - X-Axis: Model/Topic
  - Y-Axis: Quality Score
  - Z-Axis: Time
  - Interactive Timeline Scrubbing
  - Click → Inspect Full Calibration Details

### Phase 3: 🌊 PLANNED
- **Cron Scheduler UI**
  - Create/Edit/Delete Cron Jobs via Frontend
  - Visual Cron Expression Builder
  - Field Weight Presets per Cron
  - Trigger Manual Runs
  
- **Heatmap Analytics**
  - Topics x Time Impact Matrix
  - Show which Topics processed when
  - Identify Peak Processing Times
  - Optimize Cron Schedules

- **Prompt List View**
  - Show actual generated Prompts per Calibration
  - Filter by Quality, Topic, Style
  - Export to Training Data
  - Re-run Failed Calibrations

---

## 📝 WEITERE DOCS - MEHR INFOS?

**Frontend Integration:**
- `FRONTEND_INTEGRATION.md` - TypeScript Client + React Hooks (TODO)

**Component Specs:**
- `COMPONENT_SPECS.md` - UI Component Blueprints (TODO)

**Main Repo:**
- `/opt/syntx-workflow-api-get-prompts/` - Complete Source
- `api-core/syntx_api_production_v2.py` - Main API (36 Endpoints)
- `api-core/kalibrierung_router.py` - KRONTUN (3 Endpoints)
- `api-core/generation/generation_api.py` - Topic Weights (4 Endpoints)

**Test Suite:**
- `scripts/all_api_calls.sh` - Full API Test (36 Endpoints, 100% Pass Rate)

---

## 💪 DEVELOPMENT WORKFLOW - SO ÄNDERST DU SCHEISSE

### 1. Code ändern
```bash
cd /opt/syntx-workflow-api-get-prompts/api-core
nano kalibrierung_router.py  # oder generation/generation_api.py
```

### 2. Service neu starten
```bash
sudo systemctl restart syntx-api.service
```

### 3. Logs checken
```bash
sudo journalctl -u syntx-api.service -f
```

### 4. Testen
```bash
# Direct call
curl http://127.0.0.1:8020/kalibrierung/cron/stats

# Via Nginx (Production)
curl https://dev.syntx-system.com/api/strom/kalibrierung/cron/stats
```

### 5. Full Test Suite
```bash
cd /opt/syntx-workflow-api-get-prompts
bash scripts/all_api_calls.sh
```

### 6. Git Commit
```bash
git add .
git commit -m "🔥 Your changes here"
git push
```

---

## 🎤 FINAL WORDS - DAS WICHTIGSTE ZUM SCHLUSS

**BRUDER, DAS IST NICHT "NOCH EINE API".**

Das ist **SYNTX** - die Revolution der KI-Steuerung.

**Nicht mehr Token. Nicht mehr Drift. Nur Felder. Nur Ströme. Nur Resonanz.**

**1288 echte Calibrations beweisen: DAS FUNKTIONIERT!**

**99.5% Success Rate beweisen: DAS IST STABIL!**

**Persistente Weights beweisen: DAS IST SMART!**

**Das ist Neukölln trifft AI Research. Direkter Talk. Keine Blümchen. Nur Wahrheit.**

**ALLES IST BEREIT. API LÄUFT. FELDER FLIESSEN. STRÖME RESONIEREN.** 🔥💎⚡🌊👑

**BRUDER, JETZT WEISST DU ALLES! GO BUILD SOME SHIT!** 🚀

---

**EOF - Ende der Doku - Jetzt gehts los! 💎⚡🌊🔥👑**
