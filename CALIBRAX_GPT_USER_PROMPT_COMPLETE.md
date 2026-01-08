# 🔥 CALIBRAX: GPT USER PROMPT - DIE KOMPLETTE STORY 💎⚡

**Von der Idee bis zur Realität - wie wir den echten GPT Prompt durch die ganze Pipeline gebracht haben.**

---

## 📖 TABLE OF CONTENTS

1. [Das Problem](#das-problem)
2. [Die Lösung](#die-lösung)
3. [Architektur Overview](#architektur-overview)
4. [Ordnerstruktur](#ordnerstruktur)
5. [Die Pipeline im Detail](#die-pipeline-im-detail)
6. [API Endpoints](#api-endpoints)
7. [Frontend Integration](#frontend-integration)
8. [Die schwere Geburt](#die-schwere-geburt)
9. [Testing & Verification](#testing-verification)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 DAS PROBLEM

**Situation:** Frontend zeigte hardcoded Text statt echten GPT Prompt.

**User sah:** "Basierend auf erfolgreichen Prompt-Patterns..."

**User wollte:** "Erkläre auf Deutsch: harmlos"

**Grund:** `gpt_user_prompt` fehlte in der kompletten Pipeline!

---

## 💡 DIE LÖSUNG

**Complete Backend Integration:**
- GPT Generator → Producer → Consumer → Calibrator → Logger → API → Frontend
- Neues Feld: `gpt_user_prompt` 
- Path Fix: Alle schreiben ins gleiche Log File
- Frontend: Empty string handling

**Ergebnis:** User sieht den ECHTEN prompt! ✅

---

## 🏗️ ARCHITEKTUR OVERVIEW
```
┌─────────────────────────────────────────────────────────────┐
│                    GPT-4 (OpenAI)                           │
│  Generiert Meta-Prompts für Mistral                         │
└─────────────────┬───────────────────────────────────────────┘
                  │ prompt_in: "Erkläre auf Deutsch: harmlos"
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              PRODUCER (Multilingual)                         │
│  - Ruft GPT-4 auf                                           │
│  - Speichert prompt_in als gpt_user_prompt in Job Metadata │
└─────────────────┬───────────────────────────────────────────┘
                  │ Job: queue/incoming/*.json
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                  CONSUMER                                    │
│  - Liest Job aus Queue                                      │
│  - Übergibt gpt_user_prompt an Calibrator                   │
└─────────────────┬───────────────────────────────────────────┘
                  │ meta_prompt + gpt_user_prompt
                  ▼
┌─────────────────────────────────────────────────────────────┐
│           CALIBRATOR (Enhanced)                              │
│  - Sendet meta_prompt an Mistral                            │
│  - Übergibt gpt_user_prompt an Logger                       │
└─────────────────┬───────────────────────────────────────────┘
                  │ Alle Daten
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    LOGGER                                    │
│  Schreibt JSONL Entry:                                      │
│  /opt/syntx-config/generator-data/syntex_calibrations.jsonl│
└─────────────────┬───────────────────────────────────────────┘
                  │ Log File
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              KALIBRIERUNG API                                │
│  Liest Log und exposed als REST Endpoint                    │
│  GET /api/strom/kalibrierung/cron/logs                      │
└─────────────────┬───────────────────────────────────────────┘
                  │ JSON Response
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              CALIBRAX FRONTEND                               │
│  - Fetcht von API                                           │
│  - Zeigt in GPT INPUT Modal                                 │
│  - User sieht echten Prompt! ✅                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 ORDNERSTRUKTUR
```
/opt/syntx-workflow-api-get-prompts/
├── gpt_generator/
│   └── syntx_prompt_generator.py       # GPT-4 API calls, generiert prompts
│
├── queue_system/
│   └── core/
│       ├── producer_multilingual.py     # Erstellt Jobs mit gpt_user_prompt
│       └── consumer.py                  # Verarbeitet Jobs
│
├── syntex_injector/
│   └── syntex/
│       └── core/
│           ├── calibrator.py            # Standard Calibrator
│           ├── calibrator_enhanced.py   # Enhanced (wird von Consumer genutzt)
│           └── logger.py                # Schreibt JSONL Log
│
├── api-core/
│   ├── syntx_api_production_v2.py      # FastAPI Main
│   └── kalibrierung_router.py          # /kalibrierung/* Endpoints
│
├── queue/
│   ├── incoming/*.json                  # Jobs mit Metadata
│   └── processed/*.json                 # Processed Jobs
│
└── /opt/syntx-config/generator-data/
    └── syntex_calibrations.jsonl       # MAIN LOG FILE ⚠️
```

### ⚠️ CRITICAL PATH

**Alle Komponenten schreiben/lesen aus:**
```
/opt/syntx-config/generator-data/syntex_calibrations.jsonl
```

**NICHT:**
- `./logs/syntex_calibrations.jsonl` ❌
- Irgendwo anders ❌

---

## 🔄 DIE PIPELINE IM DETAIL

### 1️⃣ GPT Generator

**File:** `gpt_generator/syntx_prompt_generator.py`

**Was es macht:**
- Ruft OpenAI GPT-4 auf
- Generiert Meta-Prompts für verschiedene Topics

**Neues Feld:** `prompt_in`

**Code:**
```python
# Line ~280, 295, 310, 325, 340, 355
return {
    "success": True,
    "prompt_sent": prompt,           # Original topic
    "prompt_in": prompt,             # 🔥 Full formatted prompt
    "prompt_generated": prompt_text,
    "quality_score": quality_score,
    "cost": cost_info
}
```

**Warum 6 Stellen?**
- Verschiedene Error Paths müssen auch `prompt_in` returnen

---

### 2️⃣ Producer

**File:** `queue_system/core/producer_multilingual.py`

**Was es macht:**
- Ruft GPT Generator auf
- Erstellt Job Files in `queue/incoming/`
- Speichert Metadata als JSON

**Neues Feld:** `gpt_user_prompt`

**Code:**
```python
# Line 108
'gpt_user_prompt': result.get('prompt_in'),  # 🔥 From GPT generator

# Line 179 - Internal method
'prompt_in': user_prompt,  # 🔥 Full user prompt
```

**Job Metadata Beispiel:**
```json
{
  "gpt_user_prompt": "Erkläre auf Deutsch: harmlos",
  "language_instruction": "Erkläre auf Deutsch:",
  "gpt_quality": {"score": 100},
  "created_at": "2026-01-08T13:34:49.357948"
}
```

---

### 3️⃣ Consumer

**File:** `queue_system/core/consumer.py`

**Was es macht:**
- Liest Jobs aus `queue/incoming/`
- Ruft Calibrator auf
- Moved Job nach `queue/processed/`

**Code:**
```python
# Line ~120
success, response, result_meta = self.calibrator.calibrate(
    meta_prompt=job.content,
    verbose=True,
    gpt_user_prompt=job.metadata.get("gpt_user_prompt")  # 🔥 Pass through
)
```

**Wichtig:** Consumer nutzt `EnhancedSyntexCalibrator`, nicht `Calibrator`!

---

### 4️⃣ Calibrator (Enhanced)

**File:** `syntex_injector/syntex/core/calibrator_enhanced.py`

**Was es macht:**
- Empfängt meta_prompt + gpt_user_prompt
- Sendet meta_prompt an Mistral
- Übergibt ALLES an Logger

**Code:**
```python
# Line 36 - Method Signature
def calibrate(
    self,
    meta_prompt: str,
    verbose: bool = True,
    gpt_user_prompt: Optional[str] = None  # 🔥 NEW!
) -> Tuple[bool, Optional[str], Dict]:

# Line ~150 - Logger Call
self.logger.log_calibration(
    meta_prompt=meta_prompt,
    full_prompt=full_prompt,
    response=response,
    success=success,
    duration_ms=duration_ms,
    retry_count=retry_count,
    error=error,
    model_params=MODEL_PARAMS,
    gpt_user_prompt=gpt_user_prompt  # 🔥 Pass to logger
)
```

---

### 5️⃣ Logger

**File:** `syntex_injector/syntex/core/logger.py`

**Was es macht:**
- Schreibt JSONL Entry
- Speichert ALLE Daten für API

**CRITICAL FIX:**
```python
# Line 13 - DEFAULT PATH
self.log_file = log_file or Path("/opt/syntx-config/generator-data/syntex_calibrations.jsonl")

# Line 28 - Method Signature
def log_calibration(
    self,
    meta_prompt: str,
    full_prompt: str,
    response: Optional[str],
    success: bool,
    duration_ms: float,
    retry_count: int = 0,
    error: Optional[str] = None,
    model_params: Optional[Dict] = None,
    gpt_user_prompt: Optional[str] = None  # 🔥 NEW!
):

# Line 46 - Log Entry
log_entry = {
    "timestamp": datetime.now(UTC).isoformat(),
    "gpt_user_prompt": gpt_user_prompt,  # 🔥 Store it
    "meta_prompt": meta_prompt,
    "full_prompt": full_prompt,
    # ... rest
}
```

**Log Entry Beispiel:**
```json
{
  "timestamp": "2026-01-08T13:53:38.572998Z",
  "gpt_user_prompt": "Magyarázd el magyarul: grenzwertig",
  "meta_prompt": "...",
  "full_prompt": "...",
  "response": "...",
  "success": true,
  "duration_ms": 121681,
  "model_params": {...}
}
```

---

### 6️⃣ Kalibrierung API

**File:** `api-core/kalibrierung_router.py`

**Was es macht:**
- Liest JSONL Log File
- Exposed als REST Endpoint
- Strukturiert Daten als `stages`

**Code:**
```python
# Line ~50 - Reading Log
log_file = Path("/opt/syntx-config/generator-data/syntex_calibrations.jsonl")

# Line ~80 - Stages Object
"stages": {
    "gpt_user_prompt": data.get('gpt_user_prompt', ''),  # 🔥 Include it
    "gpt_system_prompt": data.get('gpt_system_prompt', ''),
    "gpt_output_meta_prompt": data.get('meta_prompt', ''),
    # ... rest
}
```

---

### 7️⃣ Frontend

**File:** `components/calibrax/stages/GPTInputView.tsx`

**Was es macht:**
- Fetcht von API
- Zeigt in Modal

**Code:**
```typescript
// Line 230
{run.stages?.gpt_user_prompt && run.stages.gpt_user_prompt.trim() !== "" 
  ? run.stages.gpt_user_prompt 
  : (run.cron_data.name || "No prompt data available")}
```

**Warum kompliziert?**
- API kann `null`, `""`, oder echten Wert returnen
- Empty string `""` ist truthy in JS!
- Müssen explizit auf `.trim() !== ""` checken

---

## 📡 API ENDPOINTS

### GET /api/strom/kalibrierung/cron/logs

**Description:** Returns calibration logs with all pipeline data

**Parameters:**
```
?limit=100     (default: 100, max: 1000)
?offset=0      (default: 0)
```

**Request:**
```bash
curl -s 'https://dev.syntx-system.com/api/strom/kalibrierung/cron/logs?limit=1'
```

**Response:**
```json
{
  "erfolg": true,
  "logs": [
    {
      "timestamp": "2026-01-08T13:53:38.572998Z",
      "cron_data": {
        "name": "SYNTEX::TRUE_RAW Calibration",
        "modell": "mistral:latest",
        "felder": {
          "driftkorper": 1,
          "kalibrierung": 1,
          "stromung": 1
        }
      },
      "stages": {
        "gpt_user_prompt": "Magyarázd el magyarul: grenzwertig",
        "gpt_system_prompt": "SYNTEX::TRUE_RAW",
        "gpt_output_meta_prompt": "A 'grenzwertig' kifejezés...",
        "mistral_input": "Meta-prompt text...",
        "mistral_output": "\n\n### Driftkörperanalyse:...",
        "parsed_fields": {
          "driftkorper": "...",
          "kalibrierung": "...",
          "stromung": "..."
        }
      },
      "scores": {
        "overall": 100,
        "field_completeness": 100,
        "structure_adherence": 100
      },
      "meta": {
        "duration_ms": 121681,
        "retry_count": 0,
        "success": true
      }
    }
  ],
  "count": 1,
  "total": 500
}
```

**Key Fields:**
- `stages.gpt_user_prompt` ← **DAS IST ES!** 🔥
- `stages.gpt_system_prompt` ← System Prompt
- `stages.gpt_output_meta_prompt` ← Generated meta-prompt
- `stages.mistral_input` ← Was an Mistral ging
- `stages.mistral_output` ← Was Mistral zurückgab
- `stages.parsed_fields` ← Extrahierte SYNTX Felder

---

### GET /api/strom/kalibrierung/cron/stats

**Description:** Returns aggregated statistics

**Response:**
```json
{
  "erfolg": true,
  "active": 5,
  "pending": 12,
  "completed": 450,
  "failed": 3,
  "total": 470
}
```

---

## 🎨 FRONTEND INTEGRATION

### Fetch Code

**File:** `lib/calibrax/fetchCalibrations.ts`
```typescript
const API_BASE = 'https://dev.syntx-system.com/api/strom';

export async function fetchCalibrations(limit: number = 100) {
  const response = await fetch(`${API_BASE}/kalibrierung/cron/logs?limit=${limit}`);
  const data = await response.json();
  return data.logs as CalibrationRun[];
}
```

### Display Code

**File:** `components/calibrax/stages/GPTInputView.tsx`
```typescript
export function GPTInputView({ run }: { run: CalibrationRun }) {
  const gptUserPrompt = run.stages?.gpt_user_prompt 
    && run.stages.gpt_user_prompt.trim() !== "" 
    ? run.stages.gpt_user_prompt 
    : (run.cron_data.name || "No prompt data available");

  return (
    <div>
      <h3>USER PROMPT:</h3>
      <pre>{gptUserPrompt}</pre>
    </div>
  );
}
```

---

## 😭 DIE SCHWERE GEBURT

### Problem 1: prompt_sent vs prompt_in

**Issue:** `prompt_sent` war nur Topic ("harmlos"), nicht full prompt

**Solution:** Added `prompt_in` field mit full formatted prompt

**Lesson:** Topic ≠ User Prompt! Brauchen beide!

---

### Problem 2: Old Jobs in Queue

**Issue:** Consumer processed old jobs (ohne gpt_user_prompt)

**Reason:** FIFO queue - älteste Jobs zuerst

**Solution:** Delete old jobs before testing
```bash
rm -f queue/incoming/20260108_00*.json
```

**Lesson:** Always test with FRESH data after code changes!

---

### Problem 3: Falsches Log File

**Issue:** 
- Consumer schrieb: `./logs/syntex_calibrations.jsonl`
- API las: `/opt/syntx-config/generator-data/syntex_calibrations.jsonl`

**Result:** API zeigte alte Daten, neue kamen nicht an

**Solution:** Fixed Logger default path
```python
# Before
self.log_file = log_file or Path("logs/syntex_calibrations.jsonl")

# After
self.log_file = log_file or Path("/opt/syntx-config/generator-data/syntex_calibrations.jsonl")
```

**Lesson:** CHECK PATH CONSISTENCY ACROSS ALL COMPONENTS!

---

### Problem 4: Empty String vs Null

**Issue:** API returned `""` (empty string), not `null`

**Frontend:** 
```typescript
// This doesn't work:
{run.stages?.gpt_user_prompt || fallback}

// Because "" is falsy in || operator
```

**Solution:**
```typescript
{run.stages?.gpt_user_prompt && run.stages.gpt_user_prompt.trim() !== "" 
  ? run.stages.gpt_user_prompt 
  : fallback}
```

**Lesson:** JavaScript falsy values: `false`, `0`, `""`, `null`, `undefined`, `NaN`

---

### Problem 5: CORS (Versuch)

**Issue:** Tried to add CORS headers to nginx

**Result:** Broke everything - ALL requests failed

**Solution:** Rollback! CORS not needed (localhost dev)

**Lesson:** Don't add CORS if not needed! Test incremental!

---

## ✅ TESTING & VERIFICATION

### Complete Test Sequence
```bash
# 1. Generate job
cd /opt/syntx-workflow-api-get-prompts
rm -f queue/incoming/*.json queue/incoming/*.txt

python3 -c "
from queue_system.core.producer_multilingual import MultilingualProducer
producer = MultilingualProducer()
producer.run(count=1, force=True)
"

# 2. Check job metadata
cat queue/incoming/*.json | jq '{gpt_user_prompt, created_at}'
# Expected: {"gpt_user_prompt": "Erkläre auf Deutsch: topic", ...}

# 3. Process job
python3 -c "
from queue_system.core.consumer import QueueConsumer
consumer = QueueConsumer('syntex_system', 'TEST')
consumer.process_batch(1)
"

# 4. Check log entry
tail -1 /opt/syntx-config/generator-data/syntex_calibrations.jsonl | jq '{
  timestamp,
  gpt_user_prompt,
  success
}'
# Expected: {"gpt_user_prompt": "Erkläre auf Deutsch: topic", "success": true}

# 5. Check API
curl -s 'https://dev.syntx-system.com/api/strom/kalibrierung/cron/logs?limit=1' \
  | jq '.logs[0].stages.gpt_user_prompt'
# Expected: "Erkläre auf Deutsch: topic"

# 6. Browser test
# Open http://localhost:3000
# Click newest calibration
# Open GPT INPUT modal
# Expected: Shows real prompt!
```

---

## 🔧 TROUBLESHOOTING

### gpt_user_prompt is null

**Check:**
```bash
# 1. Job metadata
cat queue/incoming/*.json | jq .gpt_user_prompt

# 2. Producer code
grep "prompt_in" queue_system/core/producer_multilingual.py

# 3. GPT generator
grep "prompt_in" gpt_generator/syntx_prompt_generator.py
```

**Fix:** Make sure all return statements have `"prompt_in": prompt`

---

### gpt_user_prompt is empty string

**Check:**
```bash
# Log file
tail -5 /opt/syntx-config/generator-data/syntex_calibrations.jsonl | jq .gpt_user_prompt
```

**Reason:** Old jobs from before fix

**Fix:** Generate new job, process it

---

### API returns old data

**Check:**
```bash
# Log file timestamp
tail -1 /opt/syntx-config/generator-data/syntex_calibrations.jsonl | jq .timestamp

# Compare with API
curl -s 'https://dev.syntx-system.com/api/strom/kalibrierung/cron/logs?limit=1' \
  | jq '.logs[0].timestamp'
```

**Reason:** API reading from different file

**Check paths:**
```bash
# Logger
grep "syntex_calibrations" syntex_injector/syntex/core/logger.py

# API
grep "syntex_calibrations" api-core/kalibrierung_router.py
```

**Must be same:** `/opt/syntx-config/generator-data/syntex_calibrations.jsonl`

---

### Frontend shows fallback text

**Check Browser Console:**
```javascript
// Get last fetch
fetch('https://dev.syntx-system.com/api/strom/kalibrierung/cron/logs?limit=1')
  .then(r => r.json())
  .then(d => console.log(d.logs[0].stages.gpt_user_prompt))
```

**Reasons:**
1. API doesn't have data yet (old job)
2. Empty string handling in frontend
3. Fetching wrong timestamp

**Fix:** Hard refresh (Ctrl+Shift+R), click newest job

---

## 📊 STATS

### Files Modified
- **Backend:** 10 files
- **Frontend:** 10 files
- **Total:** 20 files

### Lines Changed
- **Backend:** 922 insertions, 140 deletions
- **Frontend:** 3387 insertions, 7 deletions
- **Total:** 4309 insertions, 147 deletions

### Commits
1. `b33708f` - Documentation (342 lines)
2. `2ccb026` - Backend integration (10 files)
3. `020e02e` - Frontend refactor (10 files)
4. `025bb75` - Path fix (1 file)

### Duration
**~8 hours** (including debugging, testing, documentation)

---

## 🎯 LESSONS LEARNED

1. **Test with fresh data** - Old jobs will haunt you
2. **Path consistency** - Check ALL components use same path
3. **Empty string ≠ null** - Handle both in frontend
4. **FIFO queues** - Clear old test data
5. **Incremental testing** - Test each component separately
6. **Don't add CORS if not needed** - Can break everything
7. **Multiple log locations** - Find the RIGHT one
8. **Terminal commands = gold** - Always check raw data first

---

## 🚀 FUTURE IMPROVEMENTS

1. **Unified logging** - Central log config
2. **Better error messages** - More specific failures
3. **Monitoring** - Alert when gpt_user_prompt missing
4. **Tests** - Automated pipeline tests
5. **Validation** - Ensure gpt_user_prompt never null

---

## 👑 CREDITS

**Team:**
- Ottavio (SYNTX Creator, System Architect)
- Claude (Development Partner, Assistant)

**Date:** 2026-01-08

**Location:** Berlin (Neukölln Street Style 💎)

**Vibes:** SYNTX resonance, field-based thinking, TRUE_RAW

---

**SYNTX IS REAL. AND NOW YOU SEE THE REAL PROMPTS.** 🔥⚡🌊💎👑

**"Nicht mehr Token. Nur Felder. Nur Ströme. Nur Resonanz."**

---

*End of Documentation*

