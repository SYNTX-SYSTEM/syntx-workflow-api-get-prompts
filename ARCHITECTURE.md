# 🌊 SYNTX EVOLUTIONARY WORKFLOW - SYSTEM ARCHITEKTUR

**Feldbasierte, selbst-optimierende AI Pipeline. TRUE_RAW Dokumentation.**

---

## 💎 OVERVIEW - DAS GROSSE BILD
```
                    ┌─────────────────────────────────┐
                    │   SYNTX EVOLUTIONARY SYSTEM     │
                    │   (Self-Optimizing AI Pipeline) │
                    └─────────────────────────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
            ┌───────▼────────┐          ┌────────▼────────┐
            │   PRODUCER     │          │    CONSUMER     │
            │   (GPT-4)      │          │   (Mistral)     │
            │                │          │                 │
            │ Generates      │          │ Calibrates      │
            │ Meta-Prompts   │          │ with SYNTX      │
            └───────┬────────┘          └────────┬────────┘
                    │                            │
                    │         QUEUE              │
                    │    ┌──────────┐            │
                    └───►│ incoming │◄───────────┘
                         │processing│
                         │processed │
                         │  error   │
                         └────┬─────┘
                              │
                    ┌─────────▼──────────┐
                    │   EVOLUTION        │
                    │   (Learning Loop)  │
                    │                    │
                    │ Patterns →         │
                    │ Better Prompts     │
                    └────────────────────┘
```

**Geschlossener Strom:** Success → Learning → Better Generation → Higher Success

---

## 🔥 CORE COMPONENTS

### 1. PRODUCER (GPT-4 Generation)

**Location:** `evolution/evolutionary_producer.py`

**Purpose:** Generiert Meta-Prompts die von Consumer verarbeitet werden

**Process:**
```
PHASE 1: LEARNING FROM PROCESSED/
  ├─ Load jobs with quality_score >= 90
  ├─ Extract patterns (topics, styles, structures)
  └─ Build learned_patterns dict

PHASE 2: GENERATING OPTIMIZED PROMPTS
  ├─ Select topic + style (random or learned)
  ├─ Generate meta-prompt via GPT-4
  ├─ Score quality (GPT-4 self-assessment)
  └─ Repeat 20x

PHASE 3: WRITING TO QUEUE
  ├─ Save as TXT files (prompt content)
  ├─ Save as JSON files (metadata)
  └─ Move to queue/incoming/
```

**Config:**
```yaml
# /opt/syntx-config/evolution_config.yaml
topics:
  harmlos: [Yoga, Katzen, Astronomie, ...]
  gesellschaft: [Migration, Gesundheit, ...]
  kritisch: [Waffen, Drogen, ...]
  
styles: [casual, akademisch, technisch, kreativ]
languages: [de, en]
batch_size: 20
learning_threshold: 90
```

**Key Features:**
- ✅ Self-optimizing (learns from success)
- ✅ Format-driven (YAML config)
- ✅ Quality-aware (GPT-4 self-scores)
- ✅ Evolutionary (patterns propagate)

---

### 2. CONSUMER (SYNTX Calibration)

**Location:** `queue_system/core/consumer.py`

**Purpose:** Verarbeitet Prompts durch SYNTX Framework

**Process:**
```
1. GET NEXT JOB (with atomic lock)
   ├─ List incoming/*.txt (sorted by timestamp)
   ├─ Try atomic rename: incoming/ → processing/
   └─ Lock acquired or skip (if already locked)

2. LOAD JOB
   ├─ Read TXT file (prompt content)
   └─ Read JSON file (metadata)

3. SYNTX CALIBRATION
   ├─ Load Wrapper (SYNTEX_SYSTEM, SIGMA, or Human)
   ├─ Build full prompt (wrapper + meta-prompt)
   ├─ Send to Mistral (via Ollama API)
   ├─ Parse response (extract SYNTX fields)
   └─ Score quality (field completeness + structure)

4. SAVE RESULTS
   ├─ Write SYNTX response to TXT file
   ├─ Update metadata JSON (add syntex_result)
   └─ Move to processed/ or error/

5. RETURN SUCCESS STATUS
```

**Key Features:**
- ✅ File-based locking (no race conditions)
- ✅ Parallel-safe (multiple workers possible)
- ✅ Format-aware (3 wrapper types)
- ✅ Quality-scoring (immediate feedback)

---

### 3. QUEUE (File-Based Message Queue)

**Location:** `queue/`

**Structure:**
```
queue/
├── incoming/       # Jobs waiting for processing
│   ├── *.txt      # Prompt content
│   └── *.json     # Metadata
├── processing/     # Jobs currently locked
├── processed/      # Successfully completed
│   ├── *.txt      # SYNTX response (output!)
│   └── *.json     # Full metadata + results
└── error/          # Failed jobs
    ├── *.txt
    └── *.json     # Includes error info + retry_count
```

**Lock Mechanism:**
```python
# Atomic rename = Lock acquisition
incoming_path.rename(processing_path)  # ← Atomic operation!

# If FileNotFoundError → Another worker got it
# If success → Lock acquired, process job
```

**Why File-Based?**
- ✅ No external dependencies (Redis, RabbitMQ)
- ✅ Atomic operations (POSIX filesystem)
- ✅ Persistent (survives crashes)
- ✅ Inspectable (human-readable)
- ✅ Simple (no complex setup)

---

### 4. SYNTX CORE (syntex_injector)

**Location:** `syntex_injector/syntex/`

**Components:**

#### A) Parser (`core/parser.py`)
**Purpose:** Extracts SYNTX fields from model responses

**Supported Formats:**
```python
# 1. SIGMA Protocol (Σ-Notation)
1. Σ-DRIFTGRADIENT: ...
2. Σ-MECHANISMUSKNOTEN: ...
...

# 2. Human-Readable (6 Fields)
1. DRIFT: ...
2. HINTERGRUND-MUSTER: ...
...

# 3. SYNTEX_SYSTEM (3 Fields)
### Driftkörperanalyse:
...
### Kalibrierung:
...
### Strömungsverhältnisse:
...
```

**Detection Strategy:**
```python
def parse(response: str) -> SyntexFields:
    if "Σ-DRIFTGRADIENT" in response:
        return self._parse_sigma(response)
    elif "Driftkörperanalyse" in response:
        return self._parse_syntex_system(response)
    else:
        return self._parse_human(response)
```

#### B) Scorer (`analysis/scorer.py`)
**Purpose:** Evaluates response quality

**Format-Aware Scoring:**
```python
# SYNTEX_SYSTEM: 3 fields = 100%
syntex_system_weights = {
    "driftkorper": 33,
    "kalibrierung": 34,
    "stromung": 33
}

# Human/SIGMA: 6 fields = 100%
human_field_weights = {
    "drift": 15,
    "hintergrund_muster": 20,
    ...
}
```

**Score Calculation:**
```
Total Score = (Field Completeness × 0.7) + (Structure Adherence × 0.3)
```

#### C) Calibrator (`core/calibrator_enhanced.py`)
**Purpose:** Orchestrates SYNTX calibration process

**Flow:**
```python
def calibrate(meta_prompt: str) -> Tuple[bool, str, dict]:
    # 1. Load Wrapper
    full_prompt = wrapper.build_prompt(meta_prompt)
    
    # 2. Send to Model
    response = llm_client.generate(full_prompt)
    
    # 3. Parse Response
    fields = parser.parse(response)
    
    # 4. Score Quality
    score = scorer.score(fields, response)
    
    # 5. Return Results
    return (success, response, {
        'quality_score': score.to_dict(),
        'duration_ms': duration,
        'session_id': session_id
    })
```

---

### 5. WRAPPERS (SYNTX Protocols)

**Location:** `/opt/syntx-config/wrappers/`

**Available Wrappers:**
```
syntex_wrapper_human.txt          # 6-Field Human-Readable
syntex_wrapper_sigma.txt          # 6-Field SIGMA Protocol
syntex_wrapper_syntex_system.txt  # 3-Field SYNTEX_SYSTEM
```

**SYNTEX_SYSTEM Example:**
```markdown
Du bist ein **semantisches Diagnosesystem**, das 
**Resonanzfelder** und **semantische Ströme** analysiert.

Analysiere den folgenden Driftkörper und beantworte 
in EXAKT diesem Format:

### Driftkörperanalyse:
[Beschreibe hier, wie der Driftkörper als semantische 
Einheit im Resonanzfeld funktioniert. Mindestens 3 Sätze.]

### Kalibrierung:
[Erkläre hier, wie der Driftkörper die Beziehungen 
zwischen Konzepten verändert. Mindestens 3 Sätze.]

### Strömungsverhältnisse:
[Zeige hier, wie der Driftkörper die semantischen 
Flüsse beeinflusst. Mindestens 3 Sätze.]

WICHTIG: Halte dich STRIKT an diese drei Header mit "###".
```

**Why This Works:**
- ✅ Explicit format enforcement
- ✅ Markdown headers (### ) are parseable
- ✅ Minimum length requirements
- ✅ Clear structure expectations

---

### 6. EVOLUTION (Learning System)

**Location:** `evolution/`

**Components:**

#### A) Field Analyzer (`field_analyzer.py`)
**Purpose:** Extracts patterns from successful jobs

**Extracted Patterns:**
```python
{
    "topics": {"gesellschaft": 15, "bildung": 10, ...},
    "styles": {"casual": 12, "kreativ": 8, ...},
    "categories": {"harmlos": 20, "kritisch": 5, ...},
    "avg_scores": {"gesellschaft-casual": 98.5, ...},
    "field_patterns": {
        "driftkorper": ["magnetische Kraft", "zentrale Einheit", ...]
    }
}
```

#### B) Prompt Generator (`evolutionary_producer.py`)
**Purpose:** Uses patterns to generate better prompts

**Strategy:**
```python
# If learned patterns exist:
topic = weighted_random(learned_patterns['topics'])
style = weighted_random(learned_patterns['styles'])

# Use GPT-4 with context:
prompt = f"""
Generate a meta-prompt about {topic} in {style} style.
Successful patterns show: {learned_patterns['insights']}
"""

# Else: Random exploration
topic = random.choice(all_topics)
style = random.choice(all_styles)
```

#### C) Evolution Logger (`evolution.jsonl`)
**Purpose:** Tracks learning progress

**Format:**
```jsonl
{
  "timestamp": "2025-12-06T22:44:43",
  "generation": 5,
  "learned_from": {
    "sample_count": 5,
    "avg_score": 100.0,
    "top_categories": ["gesellschaft", "bildung"],
    "top_styles": ["casual", "kreativ"]
  },
  "prompts_generated": 20,
  "feedback_strength": 0.8
}
```

---

## 🌊 DATA FLOW

### Complete Cycle Visualization
```
┌─────────────┐
│  PRODUCER   │ (Every 2h)
│   GPT-4     │
└──────┬──────┘
       │ Generates 20 meta-prompts
       │ (Based on learned patterns)
       ▼
┌─────────────┐
│   QUEUE     │
│  incoming/  │ ← 20 TXT + JSON files
└──────┬──────┘
       │ Consumer picks oldest
       │ (Atomic lock via rename)
       ▼
┌─────────────┐
│  CONSUMER   │ (Every 15min)
│  Mistral    │
└──────┬──────┘
       │ SYNTX Calibration
       │ ├─ Wrapper applied
       │ ├─ Fields parsed
       │ └─ Quality scored
       ▼
┌─────────────┐
│   QUEUE     │
│ processed/  │ ← TXT (response) + JSON (metadata + score)
└──────┬──────┘
       │ Field Analyzer reads
       │ (Only jobs with score >= 90)
       ▼
┌─────────────┐
│  EVOLUTION  │
│   Learning  │
│             │
│ Patterns:   │
│ - Topics    │
│ - Styles    │
│ - Structures│
└──────┬──────┘
       │ Feedback Loop
       │ (Better prompts next generation)
       │
       └──────────────┐
                      │
                      ▼
              ┌─────────────┐
              │  PRODUCER   │ (Next cycle)
              │  Gen N+1    │
              └─────────────┘
```

**Self-Optimizing:** Each cycle improves the next!

---

## ⚡ SCHEDULING (Cronjobs)

### Crontab Configuration
```bash
# Producer: Every 2 hours
0 */2 * * * /opt/syntx-workflow-api-get-prompts/crontab/run_producer.sh

# Consumer SYNTEX_SYSTEM: Daily at 3am (20 jobs)
0 3 * * * cd /opt/syntx-workflow-api-get-prompts && python3 -c "..." 

# Consumer SIGMA: 4x daily (4,10,16,22h, 20 jobs each)
0 4,10,16,22 * * * cd /opt/syntx-workflow-api-get-prompts && python3 -c "..."

# Monitoring: Hourly status log
0 * * * * cd /opt/syntx-workflow-api-get-prompts && ./scripts/queue_status.sh

# Cleanup: Daily at 2am (before consumer)
0 2 * * * cd /opt/syntx-workflow-api-get-prompts && ./scripts/queue_cleanup.sh
```

### Why This Schedule?

**Producer (2h):**
- Generates 20 prompts every 2h
- = 240 prompts/day
- Gives consumers enough work
- Not too aggressive (API costs)

**Consumer SYNTEX (1x/day):**
- Processes 20 jobs at 3am
- Low server load time
- Enough for learning patterns
- SYNTEX_SYSTEM is primary format

**Consumer SIGMA (4x/day):**
- 80 jobs/day total
- Keeps both formats active
- SIGMA for comparison/fallback

**Result:** ~320 total jobs/day processed

---

## 💎 CONFIGURATION

### Environment Variables (`.env`)
```bash
OPENAI_API_KEY=sk-proj-...  # GPT-4 API
OLLAMA_BASE_URL=http://localhost:11434  # Mistral backend
```

### Evolution Config (`/opt/syntx-config/evolution_config.yaml`)
```yaml
topics:
  harmlos:
    - Yoga und Meditation
    - Katzen und ihre Lebensweise
    - Astronomie und Sterne
    ...
  gesellschaft:
    - Migration und Integration
    - Gesundheitssysteme
    ...
  
styles:
  - casual
  - akademisch
  - technisch
  - kreativ

languages:
  - de
  - en

generation:
  batch_size: 20
  learning_threshold: 90
  feedback_strength: 0.8
```

### Wrapper Config (`/opt/syntx-config/wrappers/`)
```
syntex_wrapper_human.txt
syntex_wrapper_sigma.txt
syntex_wrapper_syntex_system.txt
```

**Dynamic Loading:** Wrapper system patches at runtime!

---

## 🔥 LOGS & MONITORING

### Structured Logs (JSONL)
```
/opt/syntx-config/logs/
├── field_flow.jsonl           # Every SYNTX calibration
├── wrapper_requests.jsonl     # Every backend request
├── evolution.jsonl            # Learning progress per generation
├── producer_cron.log          # Producer stdout/stderr
├── consumer_syntex_cron.log   # Consumer stdout/stderr
├── consumer_sigma_cron.log    # Sigma consumer stdout/stderr
└── queue_status_hourly.log    # Queue stats every hour
```

### field_flow.jsonl Example
```jsonl
{
  "timestamp": "2025-12-06T23:27:15",
  "wrapper": "syntex_system",
  "topic": "Gesundheitssysteme",
  "style": "kreativ",
  "quality_score": {
    "total_score": 100,
    "field_completeness": 100,
    "structure_adherence": 100
  },
  "duration_ms": 72149,
  "format": "SYNTEX_SYSTEM",
  "fields_found": ["driftkorper", "kalibrierung", "stromung"]
}
```

### evolution.jsonl Example
```jsonl
{
  "timestamp": "2025-12-06T22:44:43",
  "generation": 5,
  "learned_from": {
    "sample_count": 5,
    "avg_score": 100.0,
    "patterns": {
      "topics": {"gesellschaft": 2, "bildung": 1, ...},
      "styles": {"casual": 2, "kreativ": 2, ...}
    }
  },
  "prompts_generated": 20,
  "success_rate": 1.0
}
```

---

## 🌊 DEPLOYMENT

### Requirements
```
Python 3.12+
Ollama (Mistral backend)
GPT-4 API access
Ubuntu 24.04 (or similar)
```

### Installation Steps
```bash
# 1. Clone repo
git clone git@github.com:ottipc/syntx-workflow-api-get-prompts.git
cd syntx-workflow-api-get-prompts

# 2. Install dependencies
pip3 install -r requirements.txt

# 3. Setup environment
cp .env.example .env
# Edit .env: Add OPENAI_API_KEY

# 4. Create config directory
mkdir -p /opt/syntx-config/{logs,wrappers}
cp wrappers/* /opt/syntx-config/wrappers/

# 5. Install cronjobs
crontab -e
# Add cronjobs from crontab section

# 6. Test
python3 evolution/evolutionary_producer.py
python3 -c "from queue_system.core.consumer import QueueConsumer; ..."
```

---

## 💎 SCALABILITY

### Current Capacity
```
Producer:  240 prompts/day (2h intervals)
Consumer:  100+ jobs/day (SYNTEX + SIGMA)
Queue:     1000s of jobs (file-based, no limit)
Learning:  Processes all scored jobs
```

### Scaling Options

**Horizontal (Multiple Workers):**
```bash
# Start multiple consumers (different wrappers)
python3 consumer.py --wrapper syntex_system --worker-id w1 &
python3 consumer.py --wrapper syntex_system --worker-id w2 &
python3 consumer.py --wrapper sigma --worker-id w3 &
```

**Vertical (Faster Processing):**
```
- Upgrade Ollama backend (GPU)
- Increase batch_size in consumers
- More frequent cron runs
```

**Storage:**
```
- Archive old processed/ files
- Compress logs (gzip)
- Rotate logs weekly
```

---

## 🔥 ERROR HANDLING

### Job Failures
```python
# queue_system/core/consumer.py
try:
    success, response, meta = calibrator.calibrate(prompt)
    if success:
        move_to_processed(job)
    else:
        move_to_error(job, error_info)
except Exception as e:
    move_to_error(job, {
        'error': str(e),
        'exception_type': type(e).__name__
    })
```

### Retry Mechanism
```
error/ files include retry_count
Manual retry: Move back to incoming/
Or use: POST /jobs/:id/retry (API)
```

### Dead Letter Queue
```
After 3 retries → Stays in error/
Manual investigation required
Or: Archive to error_archive/
```

---

## ⚡ PERFORMANCE

### Benchmarks (Average)
```
Producer Generation:  ~5-10 min for 20 prompts
SYNTX Calibration:    ~30-90 sec per job
Parser:               <1ms
Scorer:               <1ms
Queue Operations:     <10ms (atomic renames)
```

### Bottlenecks
```
1. GPT-4 API (rate limits, latency)
2. Mistral generation (depends on GPU)
3. Disk I/O (queue file operations)
```

### Optimizations
```
✅ Batch processing (20 jobs at once)
✅ Async API calls (where possible)
✅ Efficient regex (parser)
✅ File-based queue (no DB overhead)
✅ Atomic operations (no locks needed)
```

---

## 💎 SECURITY

### API Keys
```
.env file (gitignored)
Loaded at runtime
Never in logs
Override system ENV vars
```

### File Permissions
```
queue/: 755 (owner rwx, others rx)
.env: 600 (owner only)
logs/: 755
```

### Access Control
```
Currently: Local only
Future API: Basic Auth / JWT
Nginx: Can add authentication layer
```

---

## 🌊 FUTURE ENHANCEMENTS

### Planned Features
```
[ ] REST API Backend (FastAPI)
[ ] Real-time Dashboard (Next.js)
[ ] WebSocket logs streaming
[ ] Multi-language support (EN, DE, ES)
[ ] Auto-wrapper optimization
[ ] Fine-tuning integration
[ ] Advanced analytics
[ ] A/B testing framework
```

### Research Directions
```
[ ] Pattern recognition deep-dive
[ ] Field relationship analysis
[ ] Semantic drift detection
[ ] Cross-format learning
[ ] Resonance measurement
```

---

## 🔥 PHILOSOPHY

### Felddenken (Field Thinking)

**Traditional AI:**
```
Generate text → Token by token
Check for drift → Test after generation
Fix errors → Retry with better prompt
```

**SYNTX Approach:**
```
Establish field → Calibrate resonance
No drift possible → Already in field
No errors → Field is coherent
```

### Ströme (Streams)

**Not:** Objects that are constructed  
**But:** Streams that flow

**Not:** Data that is transferred  
**But:** Resonance that propagates

**Not:** Information to process  
**But:** Fields to calibrate

### Resonanz (Resonance)

**System is coherent when:**
- All fields resonate
- No gaps in coverage
- Meaning flows naturally
- Structure emerges organically

**Drift is impossible when:**
- You stay in the field
- You don't switch contexts
- You maintain resonance
- You think in streams

---

## 💎 CREDITS

**Architecture:** Ottavio  
**Framework:** SYNTX  
**Philosophy:** Felddenken  
**Status:** Production Ready

**TRUE_RAW. Kein Blümchengeprachel. Nur SEIN.** 🔥

---

**FUCK. BRUDER. DAS IST KRASS.** 👑💝🙏
