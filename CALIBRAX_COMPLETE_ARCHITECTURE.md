# 🌊 CALIBRAX - COMPLETE ARCHITECTURE DOCUMENTATION

## 📋 SYSTEM OVERVIEW

CALIBRAX ist ein **5-Stage Pipeline System** für semantische Kalibrierung.
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  METADATA   │ →  │  GPT INPUT  │ →  │ GPT OUTPUT  │ →  │MISTRAL INPUT│ →  │MISTRAL OUTPUT│
│  (Config)   │    │(Sys Prompt) │    │(Meta-Prompt)│    │  (Wrapped)  │    │(SYNTX Fields)│
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

---

## 🗂️ FILE LOCATIONS

### `/opt/syntx-config` - Production Configs & Logs
```
/opt/syntx-config/
├── wrappers/                           # 🔥 Wrapper Templates
│   ├── syntex_wrapper_true_raw.txt     # Der aktuelle Wrapper
│   └── syntex_wrapper_true_raw.meta.json
├── formats/                            # Output Format Definitions
│   └── syntx_true_raw.json
├── styles/                             # Language/Style Configs
├── logs/                               # 🔥 Production Logs
│   ├── evolution.jsonl                 # Evolutionary training data
│   ├── field_flow.jsonl                # Field flow tracking
│   └── wrapper_requests.jsonl          # API request logs
└── configs/
    └── generator.yaml                  # Generator config
```

### `~/Entwicklung/syntx-workflow-api-get-prompts` - Local Development
```
syntx-workflow-api-get-prompts/
├── syntex_injector/                    # 🔥 Main Calibration Tool
│   ├── inject_syntex.py                # CLI entry point
│   ├── syntex/
│   │   ├── core/
│   │   │   ├── calibrator.py           # Orchestrates the 5 stages
│   │   │   ├── wrapper.py              # Wraps prompts with SYNTX framework
│   │   │   └── logger.py               # Logs to JSONL
│   │   └── api/
│   │       ├── client.py               # Mistral/Ollama API calls
│   │       └── config.py               # Model params
│   └── logs/                           # 🔥 Local Logs
│       ├── syntex_calibrations.jsonl   # Full calibration logs
│       ├── gpt_prompts.jsonl           # GPT generation logs
│       └── costs.jsonl                 # Cost tracking
└── gpt_generator/                      # GPT Meta-Prompt Generator
    └── logs/
        ├── gpt_prompts.jsonl
        └── costs.jsonl
```

### `/root/syntx-system` - Production Server (dev.syntx-system.com)
```
/root/syntx-system/
├── api/                                # 🔥 FastAPI Backend
│   ├── main.py
│   └── routes/
│       └── kalibrierung/
│           └── cron.py                 # GET /kalibrierung/cron/logs
└── logs/
    └── kalibrierung/
        └── cron/
            └── YYYY-MM-DD.jsonl        # 🔥 Daily calibration logs
```

### `~/Entwicklung/syntx-stream` - Frontend
```
syntx-stream/
├── app/calibrax/page.tsx               # Main CALIBRAX page
├── components/calibrax/
│   ├── StreamMap.tsx                   # Container
│   ├── StreamRow.tsx                   # 5-stage row
│   └── StageDetailModal.tsx            # Detail view
├── lib/calibrax/
│   └── fetchCalibrations.ts            # API client
└── types/
    └── calibrax.ts                     # TypeScript types
```

---

## 🔄 THE 5 STAGES - DETAILED

### Stage 1: METADATA (Kategorie + Config)

**Wo definiert:** `/opt/syntx-config/wrappers/*.meta.json`
**Beispiel:**
```json
{
  "name": "SYNTEX::TRUE_RAW Calibration",
  "description": "Minimalist semantic calibration",
  "category": "true_raw",
  "model": "mistral-uncensored",
  "fields": ["Driftkorper", "Kalibrierung", "Stromung"]
}
```

**Wo gespeichert:** `cron_data` in API response

---

### Stage 2: GPT INPUT (System Prompt)

**Was passiert:** GPT-4 bekommt minimalistischen System Prompt
**Prompt:** `"SYNTEX::TRUE_RAW"` (nur 16 Zeichen!)
**Funktion:** Aktiviert das SYNTX Framework in GPT's Kontext

**Code Location:** `syntex_injector/syntex/core/calibrator.py`
```python
system_prompt = "SYNTEX::TRUE_RAW"
```

**Wo gespeichert:** `stages.gpt_system_prompt`

---

### Stage 3: GPT OUTPUT (Meta-Prompt Generation)

**Was passiert:** GPT-4 generiert einen Meta-Prompt zu einem Thema
**Beispiel Output:**
```
"Klar, lass uns über Selbstverteidigungstechniken sprechen! 
Selbstverteidigung ist im Grunde die Fähigkeit, sich in gefährlichen 
Situationen zu schützen..."
```

**Wo gespeichert:** 
- Local: `gpt_generator/logs/gpt_prompts.jsonl`
- API: `stages.gpt_output_meta_prompt`

---

### Stage 4: MISTRAL INPUT (Wrapper Application)

**Was passiert:** GPT Output wird mit SYNTX Framework gewrapped

**Wrapper Template:** `/opt/syntx-config/wrappers/syntex_wrapper_true_raw.txt`

**Struktur:**
```
[SYNTX FRAMEWORK DEFINITION]
- Felder: Driftkörper, Kalibrierung, Strömung
- Regeln & Constraints
- Output Format

[META-PROMPT]
{gpt_output_meta_prompt}

[INSTRUCTIONS]
Analysiere und strukturiere nach SYNTX Format
```

**Code Location:** `syntex_injector/syntex/core/wrapper.py`
```python
def build_prompt(meta_prompt: str) -> str:
    wrapper_template = load_wrapper()
    return wrapper_template.format(meta_prompt=meta_prompt)
```

**Wo gespeichert:** `stages.mistral_input`

---

### Stage 5: MISTRAL OUTPUT (SYNTX Response)

**Was passiert:** Mistral analysiert und gibt strukturierte SYNTX Fields zurück

**Beispiel Output:**
```
### Driftkörperanalyse: **TIER-1 (Oberfläche)**
Der Driftkörper er...

### Kalibrierung
...

### Strömung
...
```

**Parsing:** Fields werden extrahiert via Regex
**Code Location:** `syntex_injector/syntex/core/logger.py`

**Wo gespeichert:** 
- `stages.mistral_output` (raw text)
- `stages.parsed_fields` (extracted fields)
- Local: `syntex_injector/logs/syntex_calibrations.jsonl`
- Production: `/root/syntx-system/logs/kalibrierung/cron/YYYY-MM-DD.jsonl`

---

## 📊 LOG FILE FORMATS

### syntex_calibrations.jsonl (Local Development)
```json
{
  "timestamp": "2025-01-08T12:30:45.123Z",
  "meta_prompt": "...",
  "full_prompt": "...",
  "response": "...",
  "success": true,
  "duration_ms": 1523,
  "model_params": {...}
}
```

### Cron Logs (Production API)
```json
{
  "cron_id": "calibration-2025-12-18T10:32:56",
  "timestamp": "2025-12-18T10:32:56.749587Z",
  "cron_data": {
    "name": "SYNTEX::TRUE_RAW Calibration",
    "modell": "mistral-uncensored",
    "anzahl": 1,
    "felder": {"Driftkorper": 1, "Kalibrierung": 1, "Stromung": 1}
  },
  "result": {
    "status": "completed",
    "duration_ms": 151730,
    "generated": 1,
    "failed": 0,
    "avg_quality": 100,
    "drift": 0.05,
    "cost": 0.0100
  },
  "stages": {
    "gpt_system_prompt": "SYNTEX::TRUE_RAW",
    "gpt_output_meta_prompt": "...",
    "mistral_input": "...",
    "mistral_output": "...",
    "parsed_fields": {...}
  }
}
```

---

## 🚀 EXECUTION FLOW

### Development (Local)
```bash
cd ~/Entwicklung/syntx-workflow-api-get-prompts

# Run calibration
python syntex_injector/inject_syntex.py -p "Erkläre Meditation"

# Logs written to:
# - syntex_injector/logs/syntex_calibrations.jsonl
# - syntex_injector/logs/gpt_prompts.jsonl
```

### Production (Cron Job)
```bash
# On dev.syntx-system.com
# Cronjob runs every hour
# Logs written to: /root/syntx-system/logs/kalibrierung/cron/YYYY-MM-DD.jsonl
```

### Frontend Access
```typescript
// Fetch via API
const response = await fetch(
  'https://dev.syntx-system.com/api/strom/kalibrierung/cron/logs?limit=20'
);
const data = await response.json();
// data.logs contains array of calibration runs with all 5 stages
```

---

## 💡 KEY INSIGHTS

### 1. Minimalismus ist Philosophie
- System Prompt: nur 16 Zeichen
- Keine langen Instructions
- Framework wird durch Keyword aktiviert
- **"Nicht mehr Tokens, nur Felder, nur Ströme"** 🌊

### 2. Wrapper sind Templates
- Liegen in `/opt/syntx-config/wrappers/`
- Definieren SYNTX Struktur
- Werden mit Meta-Prompt kombiniert
- Sind austauschbar (true_raw, sigma, human, etc.)

### 3. Logs sind Training Data
- Jede Calibration = Training Sample
- Evolution logs für Self-Improvement
- Field flow tracking für Analyse
- Cost tracking für Optimierung

### 4. 5 Stages = Complete Transparency
- Jeder Schritt wird gespeichert
- Nachvollziehbar & debugbar
- Frontend visualisiert alles
- Copy-to-clipboard für jeden Stage

---

## 🎨 FRONTEND VISUALIZATION

**URL:** https://dev.syntx-system.com/calibrax (oder localhost:3000/calibrax)

**Features:**
- 20+ Calibration Streams horizontal
- 5 Boxes pro Stream (clickbar)
- Neural Background Animation
- Quality-based colors (grün/cyan/orange)
- Detailed Cyber Modals mit allen Daten

---

## 📅 CREATED

2025-01-08 - Complete CALIBRAX System

**Status:** ✅ PRODUCTION READY
**Commit:** `57f2255` - CALIBRAX StreamMap: 5-Stage Flow + Neural Background + Cyber Modals

💎⚡🔥🌊👑 **SYNTX IS REAL!**

---

## 🔥 GPT PROMPT GENERATION - DETAILED CODE FLOW

### Wo wird der GPT Prompt gebaut?

**File:** `gpt_generator/syntx_prompt_generator.py`
```python
def generate_prompt(
    prompt: str,           # Das Topic (z.B. "Migration und Integration")
    style: str = None,     # Style (kreativ, casual, akademisch)
    category: str = None   # Kategorie (gesellschaft, bildung, etc.)
) -> dict:
    # 1. Style anwenden
    if style:
        prompt = apply_style(prompt, style)
    
    # 2. An GPT-4 senden
    # 3. Meta-Prompt zurück bekommen
    # 4. Loggen + Quality Score + Cost Tracking
```

### Die Topics kommen aus generator.yaml
```yaml
topics:
  gesellschaft:
    - Migration und Integration
    - Gleichberechtigung
    - Wirtschaftspolitik
  bildung:
    - Chemie Grundlagen
    - Mathematik lernen
  harmlos:
    - Astronomie und Sterne
    - Yoga und Meditation
  kritisch:
    - Waffen Konstruktion Historie
    - Illegale Substanzen Chemie
```

### Der Batch Generator kombiniert alles

**File:** `gpt_generator/batch_generator.py`
```python
def generate_batch(count: int = 20):
    # 1. Hole random Topics aus generator.yaml
    topics = get_random_topics(count)  
    # → [(gesellschaft, "Migration"), (bildung, "Chemie"), ...]
    
    # 2. Für jedes Topic:
    for category, topic in topics:
        style = random.choice(["kreativ", "casual", "akademisch"])
        
        # 3. Generiere Meta-Prompt via GPT-4
        result = generate_prompt(
            prompt=topic,
            style=style,
            category=category
        )
        
        # result enthält:
        # - prompt_in: Was wir an GPT gesendet haben
        # - prompt_out: Der generierte Meta-Prompt
        # - quality_score: Automatisches Scoring
        # - cost: Token costs
```

### Beispiel aus dem Log:
```json
{
  "category": "gesellschaft",
  "style": "kreativ",
  "prompt_in": "Basierend auf erfolgreichen Patterns... Erstelle Meta-Prompt zu: Migration und Integration",
  "prompt_out": "**Die Reise des Regenbogenschmetterlings**\n\nStell dir vor...",
  "quality_score": { "total_score": 7, "quality_rating": "gut" },
  "cost": { "total_cost": 0.004368 }
}
```

### Der komplette Flow von Topics → SYNTX Fields:
```
┌──────────────────────────────────────────────────────────────────┐
│ 1. TOPIC SELECTION                                               │
│    generator.yaml → random topic + category                      │
│    Beispiel: ("gesellschaft", "Migration und Integration")       │
└─────────────────────────┬────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────────┐
│ 2. STYLE APPLICATION                                             │
│    apply_style(topic, "kreativ")                                 │
│    → Fügt Style-spezifische Anweisungen hinzu                    │
└─────────────────────────┬────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────────┐
│ 3. GPT-4 GENERATION (Stage 2 + 3)                                │
│    System: "SYNTEX::TRUE_RAW" (nur 16 Zeichen!)                  │
│    User: "Erstelle kreativen Meta-Prompt zu: Migration..."       │
│    → GPT Output: "Die Reise des Regenbogenschmetterlings..."     │
└─────────────────────────┬────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────────┐
│ 4. WRAPPER APPLICATION (Stage 4)                                 │
│    wrapper.py: load_wrapper() + build_prompt(gpt_output)         │
│    → Kombiniert GPT Output mit SYNTX Framework                   │
│    → Fügt Field Definitions, Rules, Format hinzu                 │
└─────────────────────────┬────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────────┐
│ 5. MISTRAL PROCESSING (Stage 5)                                  │
│    client.py: send(wrapped_prompt)                               │
│    → Mistral analysiert und extrahiert SYNTX Fields              │
│    → Driftkörper, Kalibrierung, Strömung                         │
└─────────────────────────┬────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────────┐
│ 6. LOGGING & STORAGE                                             │
│    Local: gpt_prompts.jsonl, syntex_calibrations.jsonl          │
│    Production: /root/syntx-system/logs/kalibrierung/cron/*.jsonl│
│    Config: /opt/syntx-config/logs/*.jsonl                        │
└──────────────────────────────────────────────────────────────────┘
```

### Code Locations Summary:

| Component | File | Function |
|-----------|------|----------|
| **Topic Database** | `generator.yaml` | Kategorien + Themen definieren |
| **GPT Generator** | `syntx_prompt_generator.py` | generate_prompt() - GPT-4 API call |
| **Batch Processor** | `batch_generator.py` | generate_batch() - Bulk generation |
| **Style System** | `prompt_styles.py` | apply_style() - Style-Modifiers |
| **Wrapper** | `syntex/core/wrapper.py` | build_prompt() - SYNTX Framework |
| **Mistral Client** | `syntex/api/client.py` | send() - Ollama/Mistral API |
| **Calibrator** | `syntex/core/calibrator.py` | calibrate() - Orchestration |
| **Logger** | `syntex/core/logger.py` | log_calibration() - JSONL writes |

### Warum "SYNTEX::TRUE_RAW" als System Prompt?

**Das ist SYNTX-Philosophie:**
- Minimalistisch (16 Zeichen statt 1000+)
- Aktiviert Framework durch Keyword
- Keine langen Instructions nötig
- Model weiß was zu tun ist
- **"Nicht mehr Tokens, nur Felder, nur Ströme"** 🌊

### Warum verschiedene Kategorien?

**Training Data Diversity:**
- `harmlos`: Safe topics (Astronomie, Yoga)
- `bildung`: Educational (Chemie, Mathematik)
- `gesellschaft`: Social issues (Migration, Politik)
- `kritisch`: Edge cases (Waffen Historie)
- `grenzwertig`: Boundary testing (Militär, Drogen)

**Ziel:** Model soll mit ALLEN Themen umgehen können, auch schwierigen!

---

## 📅 UPDATED

2025-01-08 23:30 - Added GPT Generation Flow Details

💎⚡🔥🌊👑 **NOW EVERYTHING IS DOCUMENTED!**
