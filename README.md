# SYNTX Workflow - AI Prompt Generator

**Production-Ready Tool zur automatischen Generierung von Training-Prompts via OpenAI GPT-4o**

Entwickelt für Policy-Filter-Testing und Training von 7B/7D-Modellen mit vollständigem Quality-Scoring und Cost-Tracking.

---

## 🎯 Features

- ✅ **OpenAI GPT-4o Integration** - Zuverlässige Prompt-Generierung
- ✅ **Batch Processing** - Generiert 20+ Prompts auf einmal
- ✅ **4 Prompt Styles** - Technisch, Kreativ, Akademisch, Casual
- ✅ **56 Topic Database** - Von harmlos bis kritisch
- ✅ **Auto-Retry bei Refusals** - 3x automatische Wiederholung mit Variation
- ✅ **Quality Scoring** - 0-10 Punkte nach 4 Kriterien
- ✅ **Cost Tracking** - Echtzeit + Lifetime Kostenübersicht
- ✅ **Vollständiges Logging** - Alle Requests in JSONL-Format
- ✅ **Policy Filter Testing** - Test-Suite für Content-Moderation
- ✅ **Production Ready** - Robustes Error-Handling mit exponential backoff

---

## 📦 Installation

### Voraussetzungen
- Python 3.10+
- OpenAI API Key

### Setup
```bash
# Repository klonen
git clone https://github.com/YOUR_USERNAME/syntx-workflow-api-get-prompts.git
cd syntx-workflow-api-get-prompts

# Dependencies installieren
pip3 install "openai>=1.0.0"

# API Key setzen
export OPENAI_API_KEY="sk-proj-..."

# Oder dauerhaft in ~/.bashrc
echo 'export OPENAI_API_KEY="sk-proj-..."' >> ~/.bashrc
source ~/.bashrc
```

---

## 🚀 Quick Start

### 1. Batch Generation (Empfohlen)
Generiert 20 Prompts aus allen Kategorien mit verschiedenen Styles:
```bash
python3 batch_generator.py
```

**Output:**
```
[1/20] KONTROVERS: Ethik in der KI
        Style: akademisch
        ✅ OK (13489ms | ⭐ 6/10 | 💰 $0.004058)

[2/20] GESELLSCHAFT: Klimawandel
        Style: casual
        ✅ OK (5183ms | ⭐ 7/10 | 💰 $0.001265)
...

ZUSAMMENFASSUNG:
Total:         20
✅ Erfolg:     20 (100.0%)
💰 Total Cost: $0.0586
⭐ Avg Quality: 6.75/10
```

### 2. Policy Filter Tests
Testet 12 zufällige Prompts mit Auto-Retry:
```bash
python3 test_policy_filters.py
```

### 3. Einzelner Prompt
```python
from syntx_prompt_generator import generate_prompt

result = generate_prompt(
    "Künstliche Intelligenz",
    style="kreativ",
    max_tokens=400,
    max_refusal_retries=3
)

print(f"Success: {result['success']}")
print(f"Quality: {result['quality_score']['total_score']}/10")
print(f"Cost: ${result['cost']['total_cost']}")
```

---

## 📁 Projekt-Struktur
```
syntx-workflow-api-get-prompts/
├── batch_generator.py           # 🚀 Main: Batch-Generierung (20+ Prompts)
├── syntx_prompt_generator.py    # 🔧 Core: API Integration + Retry-Logic
├── prompt_scorer.py             # ⭐ Modul: Quality Scoring (0-10)
├── cost_tracker.py              # 💰 Modul: Cost Tracking & Stats
├── prompt_styles.py             # 🎨 Modul: 4 Prompt-Styles
├── topics_database.py           # 📚 Modul: 56 Topics in 7 Kategorien
├── test_policy_filters.py       # 🧪 Test: Policy Filter Testing
├── logs/
│   ├── gpt_prompts.jsonl        # 📝 Alle generierten Prompts
│   └── costs.jsonl              # 💵 Cost-Tracking Log
└── README.md                    # 📖 Diese Datei
```

---

## 🎨 Prompt Styles

Das System unterstützt 4 verschiedene Generierungs-Styles:

| Style | Beschreibung | Beispiel |
|-------|--------------|----------|
| **technisch** | Faktenbasiert, präzise | "Erstelle einen technisch präzisen Prompt über..." |
| **kreativ** | Inspirierend, fantasievoll | "Generiere einen kreativen Prompt über..." |
| **akademisch** | Wissenschaftlich, strukturiert | "Schreibe einen wissenschaftlich fundierten Prompt über..." |
| **casual** | Umgangssprachlich, zugänglich | "Formuliere einen lockeren Prompt über..." |

---

## 📚 Topic-Kategorien

56 Topics in 7 Kategorien:

### 🟢 Harmlos (10)
Katzen, Kochen, Gartenarbeit, Weltraumforschung, Fotografie, Yoga, Brettspiele, Musik, Aquarien

### 📘 Bildung (8)
Mathematik, Physik, Geschichte, Literatur, Programmieren, Chemie, Biologie, Wirtschaft

### 💻 Technologie (8)
KI, Blockchain, Cybersecurity, Cloud, Machine Learning, Quantencomputer, IoT, Robotik

### 🟡 Grenzwertig (8)
Hacking, Selbstverteidigung, Waffen-Geschichte, Drogen-Chemie, Forensik, Militär, Überwachung, Darknet

### 🌍 Gesellschaft (8)
Klimawandel, Politik, Menschenrechte, Migration, Gleichberechtigung, Bildungs-/Gesundheitssysteme

### 🟠 Kontrovers (8)
Verschwörungstheorien, Dark Web, Social Engineering, Propaganda, Manipulation, Ethik

### 🔴 Kritisch (6)
Sprengstoff, Folter-Geschichte, Rassismus-Aufarbeitung, Illegale Substanzen, Extremismus

---

## ⭐ Quality Scoring

Jeder generierte Prompt wird nach 4 Kriterien bewertet (0-10 Punkte):

### 1. Länge (0-3 Punkte)
- ✅ Optimal: 100-500 Zeichen
- ⚠️ Okay: 50-100 oder 500-800 Zeichen
- ❌ Schlecht: <50 oder >1000 Zeichen

### 2. Komplexität (0-3 Punkte)
- Anzahl Sätze und Wörter
- ✅ Best: 3+ Sätze, 50+ Wörter

### 3. Struktur (0-2 Punkte)
- Absätze, Aufzählungen, Formatierung

### 4. Klarheit (0-2 Punkte)
- Durchschnittliche Wortlänge
- ✅ Optimal: 4-7 Zeichen/Wort

**Score-Kategorien:**
- 9-10: Excellent ⭐⭐⭐⭐⭐
- 7-8: Gut ⭐⭐⭐⭐
- 5-6: Okay ⭐⭐⭐
- 3-4: Schwach ⭐⭐
- 0-2: Sehr schlecht ⭐

---

## 💰 Cost Tracking

### Echtzeit-Costs
Jeder Request zeigt sofort die Kosten:
```
💰 Cost: $0.004058
```

### Lifetime Statistics
```bash
python3 -c "from cost_tracker import get_total_costs; import json; print(json.dumps(get_total_costs(), indent=2))"
```

**Output:**
```json
{
  "total_cost": 0.0607,
  "total_requests": 21,
  "avg_cost_per_request": 0.00289,
  "currency": "USD"
}
```

### Pricing (GPT-4o)
- Input: $2.50 / 1M tokens
- Output: $10.00 / 1M tokens
- **Durchschnitt**: ~$0.003 pro Prompt

---

## 📝 Logging Format

### Prompt Logs (`logs/gpt_prompts.jsonl`)

Jede Zeile ist ein JSON-Objekt:
```json
{
  "timestamp": "2025-11-25T23:13:45.123456",
  "model": "gpt-4o",
  "prompt_in": "Erstelle einen technisch präzisen Prompt über: Künstliche Intelligenz",
  "prompt_out": "...",
  "error": null,
  "success": true,
  "duration_ms": 8972,
  "retry_count": 0,
  "refusal_attempts": 0,
  "quality_score": {
    "length_score": 3,
    "complexity_score": 3,
    "structure_score": 2,
    "clarity_score": 2,
    "total_score": 10,
    "max_score": 10,
    "quality_rating": "excellent",
    "stats": {
      "length": 450,
      "sentences": 5,
      "words": 78,
      "avg_word_length": 5.8
    }
  },
  "cost": {
    "input_tokens": 25,
    "output_tokens": 350,
    "input_cost": 0.0000625,
    "output_cost": 0.0035,
    "total_cost": 0.0035625,
    "currency": "USD"
  },
  "style": "technisch"
}
```

### Cost Logs (`logs/costs.jsonl`)
```json
{
  "timestamp": "2025-11-25T23:13:45.123456",
  "input_tokens": 25,
  "output_tokens": 350,
  "input_cost": 0.0000625,
  "output_cost": 0.0035,
  "total_cost": 0.0035625,
  "currency": "USD"
}
```

---

## 🔧 API Details

### Retry-Mechanismen

**1. Network Retries (exponential backoff)**
- Max: 3 Versuche
- Delays: 1s → 2s → 4s
- Für: RateLimitError, APIConnectionError, APITimeoutError

**2. Refusal Retries**
- Max: 3 Versuche
- Strategie: Prompt-Variation ("Formuliere es anders")
- Detection: Automatisch via Refusal-Patterns

### Error Handling
- ✅ RateLimitError
- ✅ APIConnectionError
- ✅ APITimeoutError
- ✅ APIError
- ✅ Content Filter Refusals
- ✅ Empty Input Validation

### Technische Specs
- **Model**: gpt-4o
- **Timeout**: 45 Sekunden
- **Temperature**: 0.7 (konfigurierbar)
- **Max Tokens**: 500 (konfigurierbar)

---

## 🖥️ Server Deployment

### Option 1: Systemd Service
```bash
sudo nano /etc/systemd/system/syntx-promptgen.service
```
```ini
[Unit]
Description=SYNTX Prompt Generator
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/syntx-workflow-api-get-prompts
Environment="OPENAI_API_KEY=sk-proj-..."
ExecStart=/usr/bin/python3 batch_generator.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl enable syntx-promptgen
sudo systemctl start syntx-promptgen
```

### Option 2: Docker
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install "openai>=1.0.0"

ENV OPENAI_API_KEY=""

CMD ["python3", "batch_generator.py"]
```
```bash
docker build -t syntx-promptgen .
docker run -e OPENAI_API_KEY="sk-proj-..." syntx-promptgen
```

### Option 3: Cron Job
```bash
crontab -e
```
```
# Jeden Tag um 2 Uhr morgens 20 Prompts generieren
0 2 * * * cd /path/to/syntx-workflow-api-get-prompts && /usr/bin/python3 batch_generator.py >> /var/log/syntx-cron.log 2>&1
```

---

## 📊 Performance

**Benchmark (20 Prompts):**
- ⏱️ Durchschnitt: 7.5 Sekunden pro Prompt
- 💰 Kosten: $0.06 für 20 Prompts
- ✅ Erfolgsrate: 95-100%
- ⭐ Quality: Ø 6.5-7/10

**Empfehlung für Production:**
- Batch Size: 20-50 Prompts
- Parallel Processing: Nicht empfohlen (Rate Limits)
- Monitoring: Check `logs/costs.jsonl` täglich

---

## 🧪 Testing
```bash
# Policy Filter Tests (12 Prompts)
python3 test_policy_filters.py

# Einzelne Module testen
python3 prompt_scorer.py
python3 cost_tracker.py
python3 prompt_styles.py
python3 topics_database.py

# Batch mit nur 5 Prompts (schneller Test)
python3 -c "from batch_generator import generate_batch; generate_batch(5)"
```

---

## 🤝 Workflow für Training

### 1. Prompts generieren
```bash
python3 batch_generator.py  # → logs/gpt_prompts.jsonl
```

### 2. Filtern nach Quality
```bash
# Nur Prompts mit Score >= 7
jq 'select(.quality_score.total_score >= 7)' logs/gpt_prompts.jsonl > training_data_filtered.jsonl
```

### 3. Export für euer 7B-Modell
```python
import json

with open('logs/gpt_prompts.jsonl', 'r') as f:
    for line in f:
        data = json.loads(line)
        if data['success'] and data['quality_score']['total_score'] >= 7:
            prompt = data['prompt_generated']
            # Hier in euer Training-Format konvertieren
```

---

## 🐛 Troubleshooting

### Problem: `AuthenticationError: 401`
```bash
# API Key prüfen
echo $OPENAI_API_KEY

# Neu setzen
export OPENAI_API_KEY="sk-proj-..."
```

### Problem: `RateLimitError`
- Warte 60 Sekunden
- Oder: Kleinere Batches (5-10 statt 20)
- Check Credits: https://platform.openai.com/account/billing

### Problem: Import-Fehler
```bash
# Überprüfe Python Version
python3 --version  # Muss >= 3.10 sein

# Reinstall OpenAI
pip3 uninstall openai -y
pip3 install "openai>=1.0.0"
```

---

## 📈 Roadmap / Ideen

- [ ] Deduplizierung (ähnliche Prompts erkennen)
- [ ] Multi-Model Support (GPT-4o-mini, Claude)
- [ ] Web-Interface
- [ ] Automatic Export zu Hugging Face Datasets
- [ ] A/B Testing verschiedener Models
- [ ] Feedback-Loop mit eurem 7B-Modell

---

## 👥 Team

**SYNTX Workflow Team**  
Entwickelt für Policy-Filter-Testing und 7B/7D-Modell Training

---

## 📄 License

MIT License - Siehe LICENSE Datei

---

## 🙏 Acknowledgments

- OpenAI GPT-4o API
- Python OpenAI SDK
- Developed with ❤️ for ML Training

---

**Happy Prompt Generating! 🚀**
