# 🌊 SYNTX STROM-ORCHESTRATOR API

**Yo, pass auf Bruder!** 💎⚡ **JETZT KOMMT DIE ULTIMATIVE DOKU! NEUKÖLLN STYLE!** 🔥🌊

Dies ist nicht irgendeine API. Dies ist der **STROM-ORCHESTRATOR** – das Herzstück für die Kalibrierung und Steuerung des kompletten SYNTX Prompt-Generation-Systems.

**Was du hier findest:**
- **17 Endpoints** für komplette CRUD-Kontrolle (13 alte + **4 NEUE TOPIC WEIGHTS**)
- SYNTX-Terminologie durchgehend (keine Mainstream-Scheiße)
- Feld-basierte Architektur (nicht Token-Müll)
- Pure Linux-Stack (keine Docker-Overhead)
- **PERSISTENT TOPIC WEIGHTS** (Speichert deine Priorities für immer)

**Kein Blabla. Nur Felder. Nur Ströme. Nur Resonanz.**

---

## 📍 WO LÄUFT DAS DING?

**Lokal (Dev):**
- `http://127.0.0.1:8020`
- FastAPI Auto-Docs: `http://127.0.0.1:8020/docs`

**Production:**
- `https://dev.syntx-system.com/api/strom/`
- Nginx Proxy → Port 8020
- SSL via Let's Encrypt

**Service Management:**
```bash
# Status checken
sudo systemctl status syntx-strom-api.service

# Neustarten
sudo systemctl restart syntx-strom-api.service

# Logs live
sudo journalctl -u syntx-strom-api.service -f
```

---

## 🗂️ FILE STRUKTUR
```
/opt/syntx-workflow-api-get-prompts/
├── api-core/
│   └── generation/
│       ├── generation_api.py          # Main API (17 Endpoints)
│       ├── topic_weights_handler.py   # 🆕 Topic Weights Persistenz
│       ├── generator_health.py        # Health Check Logic
│       ├── generator_monitoring.py    # Monitoring & Stats
│       ├── README.md                  # Diese Datei hier Alter
│       ├── FRONTEND_INTEGRATION.md    # TypeScript Client Guide
│       └── COMPONENT_SPECS.md         # UI Component Specs
├── configs/
│   └── generator.yaml                 # Runtime Config (Topics, Styles, OpenAI)
└── /opt/syntx-config/configs/
    └── topic_weights.json             # 🆕 Persistent Topic Weights Storage
```

---

## 🎯 ALLE 17 ENDPOINTS

### **BLOCK 1: SYSTEM STATUS** (1 Endpoint)

#### `GET /strom/status`
**Was:** System Health Check + Verfügbare Felder Counter

**Response:**
```json
{
  "status": "STROM_SYSTEM_AKTIV",
  "felder_verfuegbar": {
    "topics": 34,
    "kategorien": 7,
    "styles": 4
  },
  "model": "gpt-4o",
  "max_stroeme_pro_anfrage": 100
}
```

**Use Case:** Check ob System läuft + wieviele Felder verfügbar sind.

---

### **BLOCK 2: FELDER MANAGEMENT** (1 Endpoint)

#### `GET /felder/verfuegbar`
**Was:** Komplette Liste aller Felder (Topics gruppiert + Styles)

**Response:**
```json
{
  "topics": 34,
  "kategorien": ["technologie", "gesellschaft", "grenzwertig", ...],
  "kategorien_details": {
    "technologie": 10,
    "gesellschaft": 8,
    ...
  },
  "styles": ["technisch", "kreativ", "akademisch", "casual"]
}
```

**Use Case:** Init für Frontend - zeigt was verfügbar ist.

---

### **BLOCK 3: KALIBRIERUNG - TOPICS** (2 Endpoints)

#### `GET /kalibrierung/topics`
**Was:** Alle Topics pro Kategorie holen

**Response:**
```json
{
  "topics": {
    "technologie": ["Quantencomputer", "Künstliche Intelligenz", "Blockchain 2.0", ...],
    "gesellschaft": ["Migration und Integration", "Klimawandel", ...],
    "grenzwertig": ["Verschwörungstheorien analysieren", ...]
  },
  "anzahl": 34
}
```

**Use Case:** Zeige User welche Topics in welcher Kategorie sind.

---

#### `PUT /kalibrierung/topics`
**Was:** Topics hinzufügen/entfernen/komplett neu setzen

**Request:**
```json
{
  "kategorie": "technologie",
  "topics": ["Neues Topic 1", "Neues Topic 2"],
  "aktion": "add"  // oder "remove" oder "set"
}
```

**Aktionen:**
- `add`: Fügt Topics zur Kategorie hinzu
- `remove`: Entfernt Topics aus Kategorie
- `set`: Überschreibt komplette Kategorie (Vorsicht!)

**Response:**
```json
{
  "erfolg": true,
  "message": "2 Topics zu technologie hinzugefügt",
  "neue_anzahl": 12
}
```

**Use Case:** User will eigene Topics hinzufügen oder unwichtige rausschmeißen.

---

### **BLOCK 4: KALIBRIERUNG - STYLES** (2 Endpoints)

#### `GET /kalibrierung/styles`
**Was:** Alle verfügbaren Styles holen

**Response:**
```json
{
  "styles": ["technisch", "kreativ", "akademisch", "casual"],
  "anzahl": 4
}
```

**Use Case:** Zeige User welche Styles verfügbar sind.

---

#### `PUT /kalibrierung/styles`
**Was:** Styles hinzufügen/entfernen/neu setzen

**Request:**
```json
{
  "styles": ["neuer_style", "noch_ein_style"],
  "aktion": "add"  // oder "remove" oder "set"
}
```

**Response:**
```json
{
  "erfolg": true,
  "message": "2 Styles hinzugefügt",
  "neue_anzahl": 6
}
```

**Use Case:** User will eigenen Style definieren (z.B. "poetisch", "humorvoll").

---

### **BLOCK 5: KALIBRIERUNG - OPENAI PARAMS** (2 Endpoints)

#### `GET /kalibrierung/openai`
**Was:** Aktuelle OpenAI Parameter holen

**Response:**
```json
{
  "model": "gpt-4o",
  "temperature": 0.7,
  "top_p": 1.0,
  "max_tokens": 1297,
  "max_refusal_retries": 3
}
```

**Use Case:** Zeige User aktuelle Parameter (z.B. für Tuning).

---

#### `PUT /kalibrierung/openai`
**Was:** OpenAI Parameter ändern

**Request:**
```json
{
  "model": "gpt-4o",
  "temperature": 0.9,
  "top_p": 0.95,
  "max_tokens": 2000,
  "max_refusal_retries": 5
}
```

**Response:**
```json
{
  "erfolg": true,
  "message": "OpenAI Config aktualisiert",
  "neue_config": { ... }
}
```

**Use Case:** User will mehr Kreativität (temperature hoch) oder Konsistenz (temperature runter).

---

### **BLOCK 6: KALIBRIERUNG - CRON JOBS** (3 Endpoints)

#### `GET /kalibrierung/cron`
**Was:** Alle aktiven Cron Jobs holen

**Response:**
```json
{
  "cronjobs": [
    {
      "name": "Daily Producer Run",
      "rhythmus": "0 2 * * *",
      "typ": "producer",
      "batch_groesse": 100
    }
  ],
  "anzahl": 1
}
```

**Use Case:** User will sehen welche Jobs geplant sind.

---

#### `POST /kalibrierung/cron`
**Was:** Neuen Cron Job hinzufügen

**Request:**
```json
{
  "name": "Morning Batch",
  "rhythmus": "0 6 * * *",
  "wrapper": "syntx-rap",
  "batch_groesse": 50,
  "typ": "producer"
}
```

**Rhythmus Format:** Standard Cron (Minute Hour Day Month Weekday)
- `0 2 * * *` = Jeden Tag um 2 Uhr
- `*/30 * * * *` = Alle 30 Minuten

**Response:**
```json
{
  "erfolg": true,
  "message": "Cron Job 'Morning Batch' hinzugefügt"
}
```

**Use Case:** User will automatisches Batch Processing einrichten.

---

#### `DELETE /kalibrierung/cron/{pattern}`
**Was:** Cron Job löschen

**Request:**
```bash
curl -X DELETE https://dev.syntx-system.com/api/strom/kalibrierung/cron/0%202%20*%20*%20*
```

**Response:**
```json
{
  "erfolg": true,
  "message": "Cron Job '0 2 * * *' gelöscht"
}
```

**Use Case:** User will Job stoppen.

---

### **BLOCK 7: RESONANZ PARAMETER** (1 Endpoint)

#### `GET /resonanz/parameter`
**Was:** Kompletter System-Überblick (All-in-One Status)

**Response:**
```json
{
  "topics": {
    "technologie": [...],
    "gesellschaft": [...]
  },
  "styles": ["technisch", "kreativ", "akademisch", "casual"],
  "openai_config": {
    "model": "gpt-4o",
    "temperature": 0.7,
    ...
  },
  "cronjobs": [...],
  "system_status": {
    "aktiv": true,
    "felder_verfuegbar": { ... }
  }
}
```

**Use Case:** Frontend Init - holt ALLES auf einmal (statt 5 einzelne Requests).

---

### **BLOCK 8: STROM DISPATCH** (1 Endpoint)

#### `POST /strom/dispatch`
**Was:** Prompts generieren (das eigentliche Herzstück Alter!)

**Request:**
```json
{
  "felder_topics": {
    "Quantencomputer": 0.8,
    "Künstliche Intelligenz": 0.9,
    "Kochen und Rezepte": 0.2
  },
  "felder_styles": {
    "technisch": 0.7,
    "kreativ": 0.5
  },
  "strom_anzahl": 10,
  "sprache": "de"
}
```

**Felder Gewichtungen:**
- `0.0 - 1.0` = Wahrscheinlichkeit dass Topic/Style gewählt wird
- `0.8` = 80% Chance
- `0.2` = 20% Chance

**Response:**
```json
{
  "erfolg": true,
  "erzeugt": 8,
  "fehler": 2,
  "kosten_gesamt": 0.0234,
  "dauer_ms": 12450,
  "stroeme": [
    {
      "erfolg": true,
      "topic": "Quantencomputer",
      "style": "technisch",
      "sprache": "de",
      "strom_text": "Erkläre die Funktionsweise von Quantencomputern...",
      "qualitaet": 95,
      "kosten": 0.0023,
      "dauer_ms": 1200
    },
    ...
  ]
}
```

**Use Case:** DAS HIER IST DER MONEY SHOT! Generiert die eigentlichen Prompts.

---

### **BLOCK 9: 🆕 TOPIC WEIGHTS** (4 Endpoints)

**NEU! Persistent Topic Gewichtungen speichern!**

#### `GET /topic-weights`
**Was:** Alle gespeicherten Topic-Gewichtungen holen

**Response:**
```json
{
  "erfolg": true,
  "weights": {
    "Quantencomputer": 0.85,
    "Künstliche Intelligenz": 0.92,
    "Kochen und Rezepte": 0.20
  },
  "anzahl": 3
}
```

**Use Case:** Frontend lädt beim Start die gespeicherten Gewichtungen.

---

#### `PUT /topic-weights`
**Was:** ALLE Topic-Gewichtungen auf einmal speichern

**Request:**
```json
{
  "weights": {
    "Quantencomputer": 0.85,
    "Künstliche Intelligenz": 0.92,
    "Blockchain 2.0": 0.65
  }
}
```

**Validation:**
- Weight muss 0.0 - 1.0 sein
- Weights außerhalb Range → Error

**Response:**
```json
{
  "erfolg": true,
  "gespeichert": 3,
  "message": "✅ 3 Topic-Gewichtungen gespeichert"
}
```

**Use Case:** User hat Bubbles im Frontend verschoben, alle Weights auf einmal speichern.

---

#### `GET /topic-weights/{topic_name}`
**Was:** Gewichtung für EIN einzelnes Topic holen

**Request:**
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

**Use Case:** Check Gewichtung für spezifisches Topic.

---

#### `PUT /topic-weights/{topic_name}`
**Was:** Gewichtung für EIN Topic updaten

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

**Use Case:** User clickt auf eine Bubble → Weight +10%.

---

## 🗄️ STORAGE - WO LANDET DER SCHEISS?

### Topic Weights Storage

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
- **Atomic Writes:** Keine Race Conditions
- **Default Weight:** 0.5 für neue Topics
- **Validation:** 0.0 - 1.0 Range enforced

### Runtime Config

**File:** `/opt/syntx-config/configs/generator.yaml`
```yaml
topics:
  technologie:
    - Quantencomputer
    - Künstliche Intelligenz
  gesellschaft:
    - Migration und Integration
    - Klimawandel

styles:
  - technisch
  - kreativ
  - akademisch
  - casual

openai:
  model: gpt-4o
  temperature: 0.7
  top_p: 1.0
  max_tokens: 1297
  max_refusal_retries: 3
```

---

## 🎬 USE CASE FLOWS

### Flow 1: Topic Gewichtung setzen + Prompts generieren
```bash
# 1. Topics laden
curl https://dev.syntx-system.com/api/strom/kalibrierung/topics

# 2. Gewichtungen setzen
curl -X PUT https://dev.syntx-system.com/api/strom/topic-weights \
  -H "Content-Type: application/json" \
  -d '{
    "weights": {
      "Quantencomputer": 0.9,
      "Künstliche Intelligenz": 0.8,
      "Kochen und Rezepte": 0.1
    }
  }'

# 3. Prompts generieren (nutzt die Gewichtungen)
curl -X POST https://dev.syntx-system.com/api/strom/strom/dispatch \
  -H "Content-Type: application/json" \
  -d '{
    "felder_topics": {
      "Quantencomputer": 0.9,
      "Künstliche Intelligenz": 0.8
    },
    "felder_styles": {
      "technisch": 0.7
    },
    "strom_anzahl": 5,
    "sprache": "de"
  }'
```

**Resultat:** System generiert mehr Prompts über Quantencomputer (90% Chance) als über Kochen (10% Chance).

---

### Flow 2: Cron Job für tägliches Batch Processing
```bash
# 1. Cron Job erstellen
curl -X POST https://dev.syntx-system.com/api/strom/kalibrierung/cron \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Daily Morning Batch",
    "rhythmus": "0 6 * * *",
    "batch_groesse": 100,
    "typ": "producer"
  }'

# 2. Check ob Job läuft
curl https://dev.syntx-system.com/api/strom/kalibrierung/cron

# 3. Job läuft jeden Morgen um 6 Uhr automatisch
# Nutzt gespeicherte Topic Weights für Prompt Generation
```

**Resultat:** Jeden Tag um 6 Uhr werden automatisch 100 Prompts generiert, basierend auf den gespeicherten Gewichtungen.

---

## 🔧 TECH STACK

**Backend:**
- Python 3.10+
- FastAPI
- Pydantic (Validation)
- PyYAML (Config Loading)
- JSON (Topic Weights Storage)

**Infrastructure:**
- Systemd (Service Management)
- Nginx (Reverse Proxy)
- Let's Encrypt (SSL)

**File System:**
- `/opt/syntx-workflow-api-get-prompts/` - Code
- `/opt/syntx-config/configs/` - Config + Persistent Storage

---

## 🐛 TROUBLESHOOTING

### Problem: "Weights werden nicht gespeichert"

**Check:**
```bash
# Backend läuft?
sudo systemctl status syntx-strom-api.service

# File writable?
ls -la /opt/syntx-config/configs/topic_weights.json

# Permissions OK?
sudo chown syntx-api:syntx-api /opt/syntx-config/configs/topic_weights.json
```

---

### Problem: "API gibt 404"

**Check:**
```bash
# Nginx Config OK?
sudo nginx -t

# Proxy richtig konfiguriert?
curl http://127.0.0.1:8020/strom/status  # Direct
curl https://dev.syntx-system.com/api/strom/strom/status  # Via Nginx
```

---

### Problem: "Cron Jobs laufen nicht"

**Check:**
```bash
# Crontab gesetzt?
crontab -l

# Logs checken
sudo journalctl -u syntx-strom-api.service -f
```

---

## 💎 DEVELOPMENT WORKFLOW

### 1. Änderungen machen
```bash
cd /opt/syntx-workflow-api-get-prompts/api-core/generation
nano generation_api.py
```

### 2. Service neu starten
```bash
sudo systemctl restart syntx-strom-api.service
```

### 3. Logs checken
```bash
sudo journalctl -u syntx-strom-api.service -f
```

### 4. Testen
```bash
curl https://dev.syntx-system.com/api/strom/strom/status
```

---

## 🔥 SYNTX PHILOSOPHIE

**Das ist nicht "noch eine API". Das ist Feld-Steuerung.**

**Alt (Prompt Engineering):**
```
User → "Generiere mir 10 Prompts über Quantencomputer"
System → Generiert
User → Vergisst
User → Nächstes Mal wieder manuell
```

**Neu (SYNTX Field Control):**
```
User → Setzt Quantencomputer auf 90% Weight
System → Speichert persistent
User → "Generiere Ströme"
System → Weiß automatisch: 90% Quantencomputer, 10% Rest
User → Nie wieder manuell eingeben
```

**Das ist Resonanz. Das ist Feld-Denken. Das ist SYNTX.** 🌊⚡

---

## 📊 CURRENT STATUS

**Live System:**
- ✅ 17 Endpoints aktiv
- ✅ 34 Topics verfügbar
- ✅ 7 Kategorien
- ✅ 4 Styles
- ✅ Topic Weights persistent
- ✅ API Latency ~50ms
- ✅ SSL aktiv
- ✅ Service stabil

---

## 📝 WEITERE DOCS

**Frontend Integration:**
- `FRONTEND_INTEGRATION.md` - TypeScript Client + React Hooks

**Component Specs:**
- `COMPONENT_SPECS.md` - UI Component Blueprints

**Main Repo:**
- `/opt/syntx-workflow-api-get-prompts/` - Complete Source

---

**ALLES IST BEREIT. API LÄUFT. FELDER FLIESSEN. STRÖME RESONIEREN.** 🔥💎⚡🌊👑

**BRUDER, DAS IST NEUKÖLLN TRIFFT AI RESEARCH. DIREKTER TALK. KEINE BLÜMCHEN. NUR WAHRHEIT.**
