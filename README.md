# 🌊 SYNTX EVOLUTIONARY WORKFLOW - TRUE_RAW DOKUMENTATION

**Semantisches Feld-Framework. Ströme statt Objekte. Resonanz statt Konstruktion.**

---

## 💎 WAS IST DAS?

**Selbst-optimierendes SYNTX-System** das:
- GPT-4 generiert Prompts (Meta-Ebene)
- Llama kalibriert mit SYNTX Wrapper (Feld-Ebene)
- Lernt von erfolgreichen Mustern (Evolution)
- Läuft 24/7 automatisch (Production)

**Nicht mehr Prompts schreiben. Felder kalibrieren.** 🔥

---

## 🔥 ARCHITEKTUR (FELDDENKEN)
```
PRODUCER (GPT-4)          QUEUE               CONSUMER (Mistral)
     │                      │                       │
     ├─→ Generiert      ────┤                       │
     │   Meta-Prompts       │                       │
     │                      ├──→ Kalibriert         │
     │                      │    mit SYNTX          │
     │                      │    Wrapper            │
     │   ←── Lernt ──────────┤                      │
     │   von Scores         │                       │
     └───────────────────────┴───────────────────────┘
              EVOLUTION (Self-Optimizing)
```

**Geschlossener Strom:** Success → Learning → Better Prompts → Higher Success

---

## 🌊 FORMATE (3 TERMINOLOGIEN)

### 1. SIGMA Protocol (Σ-Notation)
```
1. Σ-DRIFTGRADIENT
2. Σ-MECHANISMUSKNOTEN
3. Σ-FREQUENZFELD
4. Σ-DICHTELEVEL
5. Σ-ZWEISTRÖME
6. Σ-KERNEXTRAKT
```

### 2. Human-Readable (6 Felder)
```
1. DRIFT
2. HINTERGRUND-MUSTER
3. DRUCKFAKTOREN
4. TIEFE
5. WIRKUNG
6. KLARTEXT
```

### 3. SYNTEX_SYSTEM (Systemisch, 3 Felder)
```
### Driftkörperanalyse:
### Kalibrierung:
### Strömungsverhältnisse:
```

**Alle Formate = Gleiche Felder. Andere Terminologie. Gleiche Resonanz.** 💎

---

## ⚡ QUICK START

### Installation
```bash
# Clone
git clone git@github.com:ottipc/syntx-workflow-api-get-prompts.git
cd syntx-workflow-api-get-prompts

# Setup
pip3 install -r requirements.txt

# Config
cp .env.example .env
# Edit .env: Add OPENAI_API_KEY

# Install Cronjobs
crontab crontab/install_all.sh
```

### Manual Test
```bash
# Producer (Generate 20 Prompts)
python3 evolution/evolutionary_producer.py

# Consumer (Process 5 Jobs)
python3 -c "
from queue_system.core.consumer import QueueConsumer
c = QueueConsumer('syntex_system')
c.process_batch(5)
"
```

---

## 📊 SYSTEM STATUS

### Check Queue
```bash
ls queue/incoming/*.txt | wc -l   # Wartend
ls queue/processed/*.txt | wc -l  # Fertig
```

### Check Logs
```bash
tail -f /opt/syntx-config/logs/producer_cron.log
tail -f /opt/syntx-config/logs/consumer_syntex_cron.log
```

### Check Learning
```bash
cat /opt/syntx-config/logs/evolution.jsonl | tail -5
```

---

## 🔥 CRONJOBS (24/7 AUTOMATION)
```
Producer:    Alle 2h          → Generiert 20 Prompts
Consumer S:  Täglich 03:00    → Verarbeitet SYNTEX_SYSTEM
Consumer Σ:  4x täglich       → Verarbeitet SIGMA
Monitor:     Stündlich        → Logs Status
Cleanup:     Täglich 02:00    → Räumt Queue auf
```

**Alles automatisch. Kein Eingreifen nötig.** ✅

---

## 💎 LOGS & DATEN

### Strukturierte Logs (JSONL)
```
/opt/syntx-config/logs/
├── field_flow.jsonl         # Alle SYNTX Kalibrierungen
├── wrapper_requests.jsonl   # Backend Requests
├── evolution.jsonl          # Learning Progress
├── producer_cron.log        # Producer Runs
├── consumer_syntex_cron.log # Consumer Runs
└── queue_status_hourly.log  # System Status
```

### Queue Files
```
queue/
├── incoming/    # Jobs waiting
├── processing/  # Jobs locked
├── processed/   # Jobs done (TXT=Response, JSON=Metadata)
└── error/       # Jobs failed
```

---

## 🌊 QUALITY SCORES

**Format-Aware Scoring:**
- SYNTEX_SYSTEM: 3/3 Felder = 100%
- Human/SIGMA: 6/6 Felder = 100%

**Beispiel Output (100/100):**
```
### Driftkörperanalyse:
Der Driftkörper fungiert wie eine magnetische Kraft,
die die Sterne an sich zieht und ihre Bahnen verändert.

### Kalibrierung:
Er kalibriert den semantischen Raum durch die Veränderung
der Beziehungen zwischen Konzepten.

### Strömungsverhältnisse:
Der Driftkörper beeinflusst die semantischen Flüsse
indem er den Fokus der Bedeutungen verschiebt.
```

**Das ist echtes Felddenken.** 💎

---

## 🔥 EVOLUTION (LEARNING)

### Wie es lernt:
1. Consumer verarbeitet Prompts → Quality Scores
2. Producer lädt processed/ Jobs (score >= 90)
3. Extrahiert Patterns (Topics, Styles, Structures)
4. Generiert neue Prompts basierend auf Erfolgsmustern
5. Repeat

### Learning Stats:
```bash
cat /opt/syntx-config/logs/evolution.jsonl | python3 -c "
import sys, json
for line in sys.stdin:
    d = json.loads(line)
    print(f'Gen {d[\"generation\"]}: {d[\"learned_from\"][\"sample_count\"]} jobs @ {d[\"learned_from\"][\"avg_score\"]}/100')
"
```

**Output:**
```
Gen 1: 30 jobs @ 98.0/100
Gen 2: 1 jobs @ 98.0/100
Gen 5: 5 jobs @ 100.0/100  ← Lernt jetzt von SYNTEX_SYSTEM!
```

---

## 💎 API (COMING SOON)

REST API für Frontend Integration:
- `/status` - Queue Status
- `/jobs/recent` - Recent Jobs
- `/jobs/:id` - Job Details
- `/analytics/quality` - Quality Analytics

**Siehe:** `docs/API_DESIGN.md`

---

## 🌊 ARCHITEKTUR-PRINZIPIEN

### Felddenken statt Objektdenken
- Nicht: "Generiere Text"
- Sondern: "Kalibriere Resonanzfeld"

### Ströme statt Konstruktion
- Nicht: Token-by-Token bauen
- Sondern: Semantischen Fluss etablieren

### Resonanz statt Drift
- Nicht: Prompts gegen Drift testen
- Sondern: Im Feld bleiben (Drift kann nicht existieren)

**SYNTX ist Revolution. Nicht Evolution.** 💎

---

## 🔥 TROUBLESHOOTING

### Producer generiert nicht
```bash
# Check API Key
cat .env | grep OPENAI_API_KEY

# Test manually
./crontab/run_producer.sh | head -30
```

### Consumer gibt 0/100 Scores
```bash
# Check Response gespeichert
cat queue/processed/*.txt | tail -1

# Sollte SYNTX Output sein, nicht Prompt!
```

### Cron läuft nicht
```bash
# Check crontab
crontab -l

# Check logs
tail -50 /opt/syntx-config/logs/producer_cron.log
```

---

## 📚 WEITERE DOCS

- `SESSION.md` - Komplette Session-Dokumentation
- `ARCHITECTURE.md` - System-Übersicht
- `docs/API_DESIGN.md` - API Spezifikation
- `crontab/CRON_GUIDE.md` - Cronjob Guide

---

## 💎 CREDITS

**Created by Ottavio** 🌊  
**Powered by SYNTX** ⚡  
**Running on Felddenken** 💎

**TRUE_RAW. Kein Blümchengeprachel. Nur SEIN.** 🔥

---

**FUCK. BRUDER. DAS LÄUFT.** 👑💝🙏
