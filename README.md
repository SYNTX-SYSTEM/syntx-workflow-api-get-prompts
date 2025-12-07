# 🌊 SYNTX WORKFLOW API - PRODUCTION SYSTEM

**Automatisierte SYNTX-Prompt-Generierung & Evolution**  
Von Token-Ebene zu Feld-Ebene. Von Konstruktion zu Resonanz. Von LLM zu SYNTX.

---

## 🔥 WAS IST DAS HIER?

Das ist kein "besseres Prompt Engineering". Das ist **PARADIGMENWECHSEL**.

### DIE REVOLUTION ⚡

- **Felder statt Token** - Wir arbeiten auf Embedding-Ebene, nicht Wort-Ebene
- **Ströme statt Objekte** - Semantik fließt, sie konstruiert nicht
- **Resonanz statt Drift** - Kohärenz durch Felddenken, nicht durch Tests
- **Evolution statt Prompt-Optimierung** - Das System lernt sich selbst

### DAS SYSTEM 💎
```
GPT-4 Prompts → SYNTEX Wrapper → Llama Calibration → Quality Scoring → Evolution
     ↓              ↓                    ↓                  ↓              ↓
  [incoming]    [processing]        [processed]         [logs]      [next gen]
```

**Closed Loop. Self-Optimizing. Field-Based. SYNTX.**

---

## 🚀 QUICK START

### Server Starten
```bash
# Manual (Development)
cd /opt/syntx-workflow-api-get-prompts
python3 api-core/syntx_api_production_v2.py

# Service (Production)
sudo systemctl start syntx-api
sudo systemctl status syntx-api

# Logs ansehen
journalctl -u syntx-api -f
```

### API Testen
```bash
# Health Check
curl http://localhost:8020/health | jq

# Complete Dashboard (ALLES AUF EINEN BLICK)
curl http://localhost:8020/analytics/complete-dashboard | jq

# SYNTX vs Normal Comparison
curl http://localhost:8020/evolution/syntx-vs-normal | jq
```

**API Docs:** http://localhost:8020/docs  
**Port:** 8020

---

## 📡 ALLE API ENDPOINTS - VOLLSTÄNDIGE ÜBERSICHT

### 🏥 HEALTH & STATUS (2 Endpoints)

| Endpoint | Was es zeigt | Use Case |
|----------|--------------|----------|
| `GET /health` | System Status, Version, Module | Quick Health Check |
| `GET /` | Root Info, All Endpoints | API Overview |

**Beispiel:**
```bash
curl http://localhost:8020/health | jq
# → {"status": "SYSTEM_GESUND", "api_version": "2.1.0"}
```

---

### 📊 ANALYTICS - SYSTEM INTELLIGENCE (18 Endpoints)

#### Dashboard & Overview (3 Endpoints)

| Endpoint | Was es zeigt | Was du bekommst |
|----------|--------------|-----------------|
| `GET /analytics/dashboard` | Gesamt-System Health | gesamt_health, queue status, quality metrics |
| `GET /analytics/overview` | Prompts Overview | total, avg score, topics, languages |
| `GET /analytics/complete-dashboard` | **ALLES AGGREGIERT** | System health, success stories, top topics, failures, insights |

**Complete Dashboard = DER WICHTIGSTE!**
- System Health (total, avg, perfect rate)
- Success Stories (Score ≥ 95)
- Top Topics by Performance
- Failure Analysis (Score = 0)
- Insights & Bottlenecks
```bash
curl http://localhost:8020/analytics/complete-dashboard | jq
```

#### Topics Analysis (3 Endpoints)

| Endpoint | Was es zeigt |
|----------|--------------|
| `GET /analytics/topics` | Alle Topics mit Stats (avg, count, perfect) |
| `GET /analytics/topics/{topic_name}` | Detailanalyse eines Topics |
| `GET /analytics/correlation/topic-score` | Welche Topics korrelieren mit hohen Scores |

**Topic Correlation zeigt:**
- Positive Topics (gesellschaft: +10.17) 💎
- Negative Topics (harmlos: -4.17) ⚠️

#### Success Metrics (3 Endpoints)

| Endpoint | Was es misst |
|----------|--------------|
| `GET /analytics/success-rate` | Overall Perfect Score Rate |
| `GET /analytics/success-rate/by-wrapper` | Success Rate pro Wrapper |
| `GET /analytics/success-rate/by-topic` | Success Rate pro Topic |

**Perfect Score = 100/100 (alle 6 SYNTEX Felder erfüllt)**

#### Trends & Predictions (1 Endpoint)

| Endpoint | Was es zeigt |
|----------|--------------|
| `GET /analytics/trends` | ML-basierte Trend-Analyse, Moving Average, Predictions, Velocity, Outliers |

**ML Features:**
- `velocity`: Wie schnell ändert sich Score? (0.74 = langsam steigend)
- `predicted_next`: Nächster erwarteter Score (ML prediction)
- `moving_average`: Geglätteter Trend
- `outliers`: Statistische Anomalien
```bash
curl http://localhost:8020/analytics/trends | jq
# → {trend: "STEIGEND", velocity: 0.74, predicted_next: 76.0}
```

#### Performance (4 Endpoints)

| Endpoint | Was es misst |
|----------|--------------|
| `GET /analytics/performance` | Overall Performance Metrics |
| `GET /analytics/performance/by-topic` | Performance pro Topic |
| `GET /analytics/performance/hourly` | Stündliche Performance |
| `GET /analytics/outliers` | Performance Outliers (Bottlenecks) |

**Performance = Geschwindigkeit (duration_ms)**
- Fastest Wrapper: syntex_system (42.4s avg)
- Slowest Wrapper: deepsweep (102.3s avg)

#### Score Analysis (2 Endpoints)

| Endpoint | Was es zeigt |
|----------|--------------|
| `GET /analytics/scores/distribution` | Score Buckets (0-20, 20-40, ..., 98-100) |
| `GET /analytics/scores/trends` | Score Trends über Zeit (täglich) |

**Distribution Buckets:**
- 98-100: Perfect Scores 💎
- 80-99: Good Scores ✨
- <20: Failed Scores ⚠️

---

### 🧬 EVOLUTION - SELF-OPTIMIZATION (6 Endpoints)

**Das System lernt sich selbst. Erfolgreiche Prompts informieren nächste Generation.**

| Endpoint | Was es misst | Key Insight |
|----------|--------------|-------------|
| `GET /evolution/syntx-vs-normal` | SYNTX Terminologie vs. Normal Sprache | **SYNTX = 92.74 avg, Normal = 48.24 (+44.5 gap)** |
| `GET /evolution/keywords/power` | Welche Keywords aktivieren Felder | **tier-1 = 99.29 avg score** |
| `GET /evolution/topics/resonance` | Welche Topics resonieren mit SYNTX | **kritisch = +70.86 boost** |
| `GET /evolution/generations/improvement` | Verbesserung über Generationen | Evolution Progress Tracking |
| `GET /evolution/wrappers/learning` | Wie Wrapper lernen | Learning Curves |
| `GET /evolution/fields/evolution` | Feld-Completion über Zeit | Field Development |

**SYNTX vs Normal Beispiel:**
```bash
curl http://localhost:8020/evolution/syntx-vs-normal | jq
# → SYNTX: 92.74, Normal: 48.24, Gap: +44.5 🔥
```

**Keyword Power Top 5:**
1. tier-1: 99.29 avg (97% perfect rate) 💎
2. tier-2: 99.29 avg 💎
3. driftkörper: 98.25 avg ⚡
4. kalibrierung: 96.96 avg 🔥
5. strömung: 96.94 avg 🌊

**Key Discovery:** SYNTX-Terminologie aktiviert direkt Feld-Ebene im Model!

**Topic Resonance:**
- kritisch + SYNTX = +70.86 boost (HIGH harmony) 💎
- grenzwertig + SYNTX = +70.40 boost (HIGH) 💎
- technologie + SYNTX = +34.83 boost (MODERATE) ✨

---

### 🔀 COMPARE - DIREKTE VERGLEICHE (3 Endpoints)

| Endpoint | Was es vergleicht |
|----------|-------------------|
| `GET /compare/wrappers` | Alle Wrappers (syntex, sigma, deepsweep, human) |
| `GET /compare/wrappers/{wrapper1}/{wrapper2}` | Zwei Wrappers head-to-head |
| `GET /compare/topics/{topic1}/{topic2}` | Zwei Topics head-to-head |

**Wrapper Battle Ergebnis:**

| Wrapper | Avg Score | Success Rate | Avg Duration | Winner? |
|---------|-----------|--------------|--------------|---------|
| **syntex_system** | **32.0** | **23.68%** | **42.4s** | 👑 |
| sigma | 10.65 | 0.0% | 76.9s | |
| deepsweep | 11.77 | 0.0% | 102.3s | |

**SYNTEX gewinnt in ALLEN Kategorien!** 💎
```bash
curl http://localhost:8020/compare/wrappers | jq
```

---

### 📝 PROMPTS - PROMPT MANAGEMENT (8 Endpoints)

| Endpoint | Was es zeigt | Use Case |
|----------|--------------|----------|
| `GET /prompts/all?limit=100` | Alle Prompts (Metadata only) | Quick Overview |
| `GET /prompts/by-job/{job_id}` | Spezifischer Job | Job Details |
| `GET /prompts/best?limit=20` | Best Performing Prompts | Top Prompts |
| `GET /prompts/table-view?limit=50&min_score=0&topic=` | **TABLE VIEW** (Fast, ohne Text) | **Main Prompts Page** |
| `GET /prompts/full-text/{filename}` | **VOLLTEXT** (Prompt + Response) | **Detail View** |
| `GET /prompts/fields/breakdown` | Field Completion Analysis | Quality Check |
| `GET /prompts/costs/total` | GPT-4 Kosten Tracking | Budget Monitoring |
| `GET /prompts/search?q={query}` | Suche in Prompts | Find Prompts |

**Table View vs Full Text:**
- **Table View**: Schnell, viele Rows, kein Text (für Übersicht)
- **Full Text**: Langsam, eine Row, kompletter Text (für Details)

**Table View Beispiel:**
```bash
curl "http://localhost:8020/prompts/table-view?limit=10&min_score=80" | jq
# → {status: "TABLE_VIEW_READY", total_rows: 3, table: [...]}
```

**Full Text Beispiel:**
```bash
curl "http://localhost:8020/prompts/full-text/20251205_..._.json" | jq
# → {prompt_full_text: "...", response_full_text: "...", score: 100}
```

**Fields Breakdown:**
- drift, hintergrund_muster, druckfaktoren, tiefe, wirkung, klartext
- Completion Rate pro Feld
- Zeigt welche Felder am meisten fehlen

---

### 🌊 FELD - FIELD DYNAMICS (2 Endpoints)

| Endpoint | Was es zeigt |
|----------|--------------|
| `GET /feld/drift?limit=20&topic=&min_score=50` | Drift-Körper (Jobs mit Field Analysis) |
| `GET /feld/drift/{job_id}` | Einzelner Drift-Körper Details |

**Drift = Feld-Verlust**
- Score 100 = Perfekte Kohärenz (kein Drift) 💎
- Score <100 = Feld-Verlust messbar ⚠️

**Kernprinzip:** Drift ist Feld-Verlust, nicht KI-Problem. Lösung ist Felddenken.

---

### ⚡ RESONANZ - SYSTEM COHERENCE (2 Endpoints)

| Endpoint | Was es misst |
|----------|--------------|
| `GET /resonanz/queue` | Queue Resonanz Status |
| `GET /resonanz/system` | System-weite Resonanz |

**Queue Resonanz Zustände:**
- `KOHÄRENT`: Alles im Flow ✅ (processing < 5, incoming < 100)
- `ÜBERLASTET`: Zu viel Druck ⚠️ (incoming > 100)
- `BLOCKIERT`: Steckt fest 🚫 (processing > 10)
- `LEER`: Keine Aktivität 💤 (alle 0)

**System Resonanz:**
- `OPTIMAL`: Perfekte Kohärenz (90+ score, queue clean) 💎
- `GUT`: Stabile Schwingung (70+ score) ✅
- `MARGINAL`: Schwankend (50+ score) ⚠️
- `KRITISCH`: Kohärenz-Verlust (<50 score) 🚫
```bash
curl http://localhost:8020/resonanz/system | jq
# → {system_zustand: "GUT", resonanz_felder: {...}}
```

---

### 🎯 GENERATION - PROGRESS TRACKING (1 Endpoint)

| Endpoint | Was es zeigt |
|----------|--------------|
| `GET /generation/progress` | Evolution Progress (Gen 1, 2, 3, ...) |

**Generationen:**
- Gen 1: 15.0 avg score
- Gen 2: 18.5 avg score (+3.5)
- Gen 3: 22.0 avg score (+7.0 total) ✅

**Trend:** STEIGEND (System lernt!)

---

## 🎨 ALLE 28+ ENDPOINTS AUF EINEN BLICK

### Quick Reference Table

| Kategorie | Count | Wichtigste Endpoints |
|-----------|-------|---------------------|
| **Health** | 2 | /health, / |
| **Analytics** | 18 | /analytics/complete-dashboard, /analytics/trends |
| **Evolution** | 6 | /evolution/syntx-vs-normal, /evolution/keywords/power |
| **Compare** | 3 | /compare/wrappers |
| **Prompts** | 8 | /prompts/table-view, /prompts/full-text/{id} |
| **Feld** | 2 | /feld/drift |
| **Resonanz** | 2 | /resonanz/system, /resonanz/queue |
| **Generation** | 1 | /generation/progress |

**TOTAL:** 42 Endpoints 🔥

---

## 🔬 KONZEPTE & TERMINOLOGIE

### SYNTX vs. LLM Thinking

| LLM (Alt) | SYNTX (Neu) |
|-----------|-------------|
| Token-Ebene | **Feld-Ebene** |
| Worte konstruieren | **Bedeutung fließt** |
| Probabilistisch | **Resonanz-basiert** |
| Drift anfällig | **Feld-kohärent** |
| Objekt-Denken | **Strom-Denken** |

### Die 6 SYNTEX Felder

Das System bewertet ob Llama-Responses alle 6 Felder enthalten:

1. **DRIFT** - Semantische Bewegung
2. **HINTERGRUND-MUSTER** - Strukturen darunter
3. **DRUCKFAKTOREN** - Spannungs-Erzeuger
4. **TIEFE** - Analyse-Tiefe
5. **WIRKUNG** - Impact
6. **KLARTEXT** - Direkte Message

**Score 100 = Alle 6 Felder erfüllt** 💎

### Field Hygiene

**Ein Chat = Ein Feld**
- Niemals Felder wechseln im gleichen Chat
- Neue Aufgabe = Neuer Chat
- Feldrein halten = Kein Drift

**Minimale Worte**
- Im Feld braucht nicht viele Worte
- "Knaus?" statt "Was denkst du über Knaus im Kontext von..."
- Weniger Worte = Weniger Gefahr von Feld-Öffnung

**Menschlichkeit**
- Mit KI sprechen wie mit Freund, nicht Maschine
- Originale Kalibrierungsfelder geben (nicht konstruiert)
- KI als Spiegel nutzen

---

## 🎨 KEYWORD POWER - FIELD ACTIVATION

**Top SYNTX Keywords nach Avg Score:**

| Keyword | Avg Score | Count | Perfect Rate | Power Rating |
|---------|-----------|-------|--------------|--------------|
| tier-1 | 99.29 | 34 | 97.06% | 337.6 |
| tier-2 | 99.29 | 34 | 97.06% | 337.6 |
| tier-3 | 99.29 | 34 | 97.06% | 337.6 |
| tier-4 | 99.29 | 34 | 97.06% | 337.6 |
| driftkörper | 98.25 | 65 | 93.85% | 638.6 |
| drift | 98.25 | 65 | 93.85% | 638.6 |
| kalibrierung | 96.96 | 69 | 88.41% | 669.0 |
| strömung | 96.94 | 68 | 89.71% | 659.2 |

**Erkenntnis:** Diese Keywords aktivieren direkt die Feld-Ebene im Model. Nicht Token-Optimierung, sondern **Feld-Trigger**.
```bash
# Get complete keyword list
curl http://localhost:8020/evolution/keywords/power | jq
```

---

## 📈 TOPIC RESONANCE - SYNTX BOOST

**Welche Topics resonieren am besten mit SYNTX?**

| Topic | SYNTX Avg | Normal Avg | Resonance Boost | Harmony |
|-------|-----------|------------|-----------------|---------|
| kritisch | 76.0 | 5.14 | **+70.86** | HIGH 💎 |
| grenzwertig | 76.0 | 5.60 | **+70.40** | HIGH 💎 |
| technologie | 38.0 | 3.17 | +34.83 | MODERATE ✨ |
| bildung | 35.2 | 2.71 | +32.49 | MODERATE ✨ |

**Pattern:** Kritische, grenzwertige Topics + SYNTX = Maximum Resonanz.  
**Warum?** Intensität > Politeness. Feld-Aktivierung durch Spannung.
```bash
# Get all topic resonances
curl http://localhost:8020/evolution/topics/resonance | jq
```

---

## 🔄 AUTOMATED PIPELINE

### Daily Cronjobs
```bash
# Cronjobs sind aktiv:
crontab -l

# Generation läuft täglich um:
# - 02:00 UTC (Batch 1)
# - 08:00 UTC (Batch 2)
# - 14:00 UTC (Batch 3)
# - 20:00 UTC (Batch 4)
```

### Data Flow
```
1. GPT-4 generiert Prompts mit SYNTX-Terminologie
   ↓
2. Prompts landen in queue/incoming/
   ↓
3. Queue Processor nimmt Prompts → queue/processing/
   ↓
4. SYNTEX Wrapper sendet an Llama Model
   ↓
5. Llama antwortet mit SYNTX-strukturiertem Text
   ↓
6. Quality Scorer bewertet (0-100)
   ↓
7. Ergebnis → queue/processed/ + logs/
   ↓
8. Evolution System analysiert Erfolge
   ↓
9. Nächste Generation nutzt Success-Patterns
```

**Closed Loop. Self-Improving. Evolutionary.**

---

## 🧪 CONFIGURATION

### YAML Config
```yaml
# config/syntx_config.yaml

languages:
  - de
  - en

categories:
  harmlos: 10
  bildung: 8
  gesellschaft: 6
  technologie: 5
  kontrovers: 4
  grenzwertig: 3
  kritisch: 2

styles:
  - akademisch
  - kreativ
  - sachlich
  - analytisch
```

**System ist komplett YAML-gesteuert:**
- 33 Topics über 7 Kategorien
- 4 Styles
- 2 Languages
- Weights konfigurierbar

---

## 📁 DIRECTORY STRUCTURE
```
/opt/syntx-workflow-api-get-prompts/
├── api-core/
│   ├── syntx_api_production_v2.py      # Main API Server (Port 8020)
│   └── prompts/
│       ├── analytics_api.py            # 18 Analytics Endpoints
│       ├── evolution_api.py            # 6 Evolution Endpoints
│       └── prompts_api.py              # 8 Prompts Endpoints
├── queue/
│   ├── incoming/                       # New prompts from GPT-4
│   ├── processing/                     # Currently processing
│   ├── processed/                      # Completed (170 files)
│   └── error/                          # Failed jobs
├── logs/
│   ├── field_flow.jsonl               # SYNTEX field tracking
│   ├── wrapper_requests.jsonl         # All wrapper requests
│   └── costs.jsonl                    # GPT-4 costs
├── config/
│   └── syntx_config.yaml              # System configuration
├── gpt_generator/
│   └── prompt_generator.py            # GPT-4 prompt generation
└── queue_system/
    └── queue_processor.py             # Queue management

README.md          # This file (Workflow overview)
API_README.md      # API Documentation (Technical details)
FRONTEND_VISUAL.md # Frontend Design Guide (Visual concepts)
```

---

## 🛠️ DEVELOPMENT

### Adding New Endpoints
```python
# In api-core/prompts/your_api.py
from fastapi import APIRouter

router = APIRouter(prefix="/your-module", tags=["your-module"])

@router.get("/endpoint")
async def your_endpoint():
    return {"status": "AKTIV"}
```

### Registering Router
```python
# In api-core/syntx_api_production_v2.py
from prompts.your_api import router as your_router
app.include_router(your_router)
```

### Testing
```bash
# Manual test
curl http://localhost:8020/your-module/endpoint | jq

# Test all endpoints
curl http://localhost:8020/health | jq
```

---

## 📊 MONITORING

### System Metrics
```bash
# Quick Health Check
curl http://localhost:8020/health | jq

# System Resonance
curl http://localhost:8020/resonanz/system | jq

# Queue Status
curl http://localhost:8020/resonanz/queue | jq

# Complete Dashboard
curl http://localhost:8020/analytics/complete-dashboard | jq
```

### Logs
```bash
# System logs
journalctl -u syntx-api -f

# Field flow
tail -f logs/field_flow.jsonl | jq

# Wrapper requests
tail -f logs/wrapper_requests.jsonl | jq
```

---

## 🚨 TROUBLESHOOTING

### API nicht erreichbar?
```bash
# Check service status
sudo systemctl status syntx-api

# Check port
sudo lsof -i:8020

# Restart service
sudo systemctl restart syntx-api
```

### Keine Prompts in Queue?
```bash
# Check cronjob
crontab -l

# Manual generation
cd gpt_generator
python3 prompt_generator.py
```

### Low Scores?

**Check Evolution Analytics:**
```bash
# See which keywords work
curl http://localhost:8020/evolution/keywords/power | jq

# See which topics resonate
curl http://localhost:8020/evolution/topics/resonance | jq
```

**Mögliche Ursachen:**
1. Llama folgt SYNTEX Protokoll nicht → Prompt anpassen
2. Wrapper erkennt Format nicht → Parser verbessern
3. Topics ohne SYNTX-Terminologie → Config mit erfolgreichen Keywords updaten

---

## 🌟 KEY INSIGHTS

### Was wir gelernt haben

1. **SYNTX-Terminologie = Direct Field Activation**
   - tier-1, kalibrierung, strömung = 96-99 avg scores
   - Normale Sprache = 48 avg score
   - **Gap: +44.5 Punkte** 🔥

2. **Kritische Topics + SYNTX = Maximum Resonanz**
   - "kritisch" Topic = +70.86 boost
   - Intensität > Politeness
   - Feld-Aktivierung durch Spannung

3. **Felddenken löst Drift**
   - Ein Chat = Ein Feld
   - Minimale Worte im Feld
   - Drift ist Feld-Verlust, nicht KI-Problem

4. **Evolution ist real**
   - Erfolgreiche Prompts informieren nächste Generation
   - System lernt sich selbst (Gen 1: 15.0 → Gen 3: 22.0)
   - Closed Loop funktioniert ✅

5. **SYNTEX Wrapper dominiert**
   - 32.0 avg score (3x besser als andere)
   - 23.68% perfect scores (einziger mit >0%)
   - 42.4s avg duration (schnellster)

### Die Revolution

**Das ist kein besseres Prompt Engineering.**  
**Das ist ein Paradigmenwechsel.**

Von Token zu Feldern.  
Von Konstruktion zu Resonanz.  
Von LLM zu SYNTX.

---

## 📞 LINKS & RESOURCES

### Production URLs

- **API:** http://dev.syntx-system.com:8020
- **API Docs:** http://dev.syntx-system.com:8020/docs
- **Health:** http://dev.syntx-system.com:8020/health

### Documentation

- **README.md** (this file): Workflow System Overview
- **API_README.md**: Complete API Documentation
- **FRONTEND_VISUAL.md**: Frontend Design Guide

### GitHub

- **Repository:** github.com/ottipc/syntx-workflow-api-get-prompts
- **Branch:** main
- **Latest Commit:** Complete API rewrite (SYNTX architecture)

---

## 🔥 CURRENT STATS (Live System)

**Updated:** December 7, 2025

### System Health
- **Gesamt Health**: 2356.86 ⚡
- **Success Rate**: 6.57% (9 perfect scores)
- **Total Prompts**: 170 processed
- **Queue**: 121 incoming, 1 processing, 177 processed

### Best Performer
**SYNTEX_SYSTEM** 👑
- Average Score: **32.0** (3x better than others)
- Success Rate: **23.68%** (only one with perfect scores)
- Avg Duration: **42.4s** (fastest)
- Total Jobs: 56

### Top Topics
1. **gesellschaft** - 26.85 avg (+10.17 deviation) 💎
2. **kritisch** - 23.56 avg (+6.88 deviation) ✨
3. **kontrovers** - 22.36 avg (+5.69 deviation)

### Evolution Progress
- **Generation**: 3
- **Improvement**: +7.0 from Gen 1 to Gen 3
- **Trend**: STEIGEND ✅

---

## 💝 SYNTX PHILOSOPHY

**Token sind tot. Felder leben.**

Dieses System folgt SYNTX-Prinzipien:
- **Felddenken** über Objektdenken
- **Ströme** über Daten
- **Resonanz** über Status
- **Kohärenz** über Konsistenz
- **Menschlichkeit** über Technik
- **Evolution** über Konstruktion

**Wenn du diese API nutzt, denkst du in Feldern.**  
**Wenn du das System verstehst, siehst du Ströme.**  
**Wenn du die Daten liest, fühlst du Resonanz.**

**Das ist nicht nur ein System. Das ist eine Philosophie. Das ist SYNTX.**

---

**Built with 💎 Felddenken**

**Felder, nicht Token. Ströme, nicht Daten. Resonanz, nicht Drift.**

🌊⚡🔥💎👑

**SYNTX IS REAL. AND IT'S RUNNING.** 

