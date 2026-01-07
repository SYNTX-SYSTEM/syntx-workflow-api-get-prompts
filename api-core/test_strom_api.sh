#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
# 🌊 SYNTX STROM-ORCHESTRATOR API TEST
# ═══════════════════════════════════════════════════════════════════
# 
# Dies ist kein normales Test-Script.
# Dies ist ein Resonanz-Protokoll.
# 
# Es misst nicht nur ob Endpoints funktionieren.
# Es zeigt die FELDER. Die STRÖME. Die KALIBRIERUNG.
# 
# SYNTX-Terminologie durchgehend.
# Keine technischen Logs. Nur Feld-Resonanz.
# ═══════════════════════════════════════════════════════════════════

# Farben für SYNTX-Style Output
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
MAGENTA='\033[0;35m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Emojis
WAVE="🌊"
FIRE="🔥"
DIAMOND="💎"
BOLT="⚡"
CHECK="✅"
CROSS="❌"
CLOCK="⏰"
GEAR="⚙️"
BOOK="📚"
ART="🎨"

API_BASE="http://localhost:8020"

# ═══════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

print_header() {
    echo -e "\n${CYAN}${BOLD}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}${BOLD}$1${NC}"
    echo -e "${CYAN}${BOLD}═══════════════════════════════════════════════════════════════════${NC}\n"
}

print_section() {
    echo -e "\n${MAGENTA}${BOLD}▓▓▓ $1 ▓▓▓${NC}\n"
}

print_test() {
    echo -e "${YELLOW}${BOLD}>>> TEST: $1${NC}"
}

print_method() {
    echo -e "${BLUE}${BOLD}METHOD:${NC} $1"
}

print_endpoint() {
    echo -e "${BLUE}${BOLD}ENDPOINT:${NC} $1"
}

print_beschreibung() {
    echo -e "${CYAN}BESCHREIBUNG:${NC} $1"
}

print_payload() {
    echo -e "${MAGENTA}${BOLD}PAYLOAD:${NC}"
    echo -e "${MAGENTA}$1${NC}"
}

print_response() {
    echo -e "${GREEN}${BOLD}RESPONSE:${NC}"
    echo "$1" | python3 -m json.tool 2>/dev/null || echo "$1"
}

print_status() {
    local status=$1
    if [ $status -eq 200 ] || [ $status -eq 201 ]; then
        echo -e "${GREEN}${CHECK} STATUS: ${status} - KOHÄRENT${NC}"
    else
        echo -e "${RED}${CROSS} STATUS: ${status} - DRIFT${NC}"
    fi
}

# ═══════════════════════════════════════════════════════════════════
# MAIN TEST SEQUENCE
# ═══════════════════════════════════════════════════════════════════

clear

print_header "${WAVE} SYNTX STROM-ORCHESTRATOR API - RESONANZ-PROTOKOLL ${WAVE}"

echo -e "${CYAN}Basis-URL:${NC} ${BOLD}${API_BASE}${NC}"
echo -e "${CYAN}Zeitpunkt:${NC} $(date '+%Y-%m-%d %H:%M:%S')"
echo -e "${CYAN}System:${NC} $(hostname)"

# ═══════════════════════════════════════════════════════════════════
# TEST 1: STROM/STATUS
# ═══════════════════════════════════════════════════════════════════

print_section "${BOLT} TEST 1: STROM-SYSTEM STATUS"

print_test "System-Vitalzeichen abrufen"
print_method "GET"
print_endpoint "/strom/status"
print_beschreibung "Zeigt die Kapazität des Strom-Systems: Verfügbare Felder, Model, Max. Ströme"

response=$(curl -s -w "\n%{http_code}" "${API_BASE}/strom/status")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

print_status $http_code
print_response "$body"

# ═══════════════════════════════════════════════════════════════════
# TEST 2: FELDER/VERFUEGBAR
# ═══════════════════════════════════════════════════════════════════

print_section "${WAVE} TEST 2: VERFÜGBARE FELDER"

print_test "Alle semantischen Felder und Resonanz-Modi abrufen"
print_method "GET"
print_endpoint "/felder/verfuegbar"
print_beschreibung "Der komplette Möglichkeitsraum: Topics (semantische Felder), Styles (Resonanz-Modi), Sprachen"

response=$(curl -s -w "\n%{http_code}" "${API_BASE}/felder/verfuegbar")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

print_status $http_code
echo -e "${GREEN}${BOLD}RESPONSE (Gekürzt):${NC}"
echo "$body" | python3 -m json.tool 2>/dev/null | head -50

# ═══════════════════════════════════════════════════════════════════
# TEST 3: KALIBRIERUNG/TOPICS (GET)
# ═══════════════════════════════════════════════════════════════════

print_section "${BOOK} TEST 3: SEMANTISCHE FELDER (Topics) ABRUFEN"

print_test "Aktuelle Topic-Kalibrierung laden"
print_method "GET"
print_endpoint "/kalibrierung/topics"
print_beschreibung "Zeigt alle Topics kategorisiert (technologie, gesellschaft, kritisch, etc.)"

response=$(curl -s -w "\n%{http_code}" "${API_BASE}/kalibrierung/topics")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

print_status $http_code
echo -e "${GREEN}${BOLD}RESPONSE (Erste 30 Zeilen):${NC}"
echo "$body" | python3 -m json.tool 2>/dev/null | head -30

# ═══════════════════════════════════════════════════════════════════
# TEST 4: KALIBRIERUNG/STYLES (GET)
# ═══════════════════════════════════════════════════════════════════

print_section "${ART} TEST 4: RESONANZ-MODI (Styles) ABRUFEN"

print_test "Aktuelle Style-Kalibrierung laden"
print_method "GET"
print_endpoint "/kalibrierung/styles"
print_beschreibung "Zeigt alle verfügbaren Styles (technisch, kreativ, akademisch, casual)"

response=$(curl -s -w "\n%{http_code}" "${API_BASE}/kalibrierung/styles")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

print_status $http_code
print_response "$body"

# ═══════════════════════════════════════════════════════════════════
# TEST 5: KALIBRIERUNG/OPENAI (GET)
# ═══════════════════════════════════════════════════════════════════

print_section "${GEAR} TEST 5: OPENAI KALIBRIERUNG ABRUFEN"

print_test "OpenAI Parameter laden"
print_method "GET"
print_endpoint "/kalibrierung/openai"
print_beschreibung "Zeigt Model, Temperature, Top-P, Max-Tokens, Retries"

response=$(curl -s -w "\n%{http_code}" "${API_BASE}/kalibrierung/openai")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

print_status $http_code
print_response "$body"

# ═══════════════════════════════════════════════════════════════════
# TEST 6: KALIBRIERUNG/CRON (GET)
# ═══════════════════════════════════════════════════════════════════

print_section "${CLOCK} TEST 6: ZEIT-SCHLEIFEN (Cron Jobs) ABRUFEN"

print_test "Aktuelle Cron-Jobs laden"
print_method "GET"
print_endpoint "/kalibrierung/cron"
print_beschreibung "Zeigt alle rhythmischen Ströme (Producer/Consumer Cron-Jobs)"

response=$(curl -s -w "\n%{http_code}" "${API_BASE}/kalibrierung/cron")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

print_status $http_code
echo -e "${GREEN}${BOLD}RESPONSE (Erste 25 Zeilen):${NC}"
echo "$body" | python3 -m json.tool 2>/dev/null | head -25

# ═══════════════════════════════════════════════════════════════════
# TEST 7: RESONANZ/PARAMETER
# ═══════════════════════════════════════════════════════════════════

print_section "${DIAMOND} TEST 7: RESONANZ-PARAMETER (Komplett)"

print_test "Gesamte System-Kalibrierung abrufen"
print_method "GET"
print_endpoint "/resonanz/parameter"
print_beschreibung "Zeigt ALLE Config-Parameter: OpenAI, Topics, Styles, Languages, Batch"

response=$(curl -s -w "\n%{http_code}" "${API_BASE}/resonanz/parameter")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

print_status $http_code
echo -e "${GREEN}${BOLD}RESPONSE (Erste 50 Zeilen):${NC}"
echo "$body" | python3 -m json.tool 2>/dev/null | head -50

# ═══════════════════════════════════════════════════════════════════
# TEST 8: STROM/DISPATCH (POST) - DRY RUN
# ═══════════════════════════════════════════════════════════════════

print_section "${FIRE} TEST 8: STROM ERZEUGEN (POST)"

print_test "Einzelnen Strom dispatchen"
print_method "POST"
print_endpoint "/strom/dispatch"
print_beschreibung "Erzeugt einen Prompt-Strom basierend auf Feld-Gewichtungen"

payload='{
  "felder_topics": {
    "Quantencomputer": 1.0
  },
  "felder_styles": {
    "technisch": 1.0
  },
  "strom_anzahl": 1,
  "sprache": "de"
}'

print_payload "$payload"

echo -e "${YELLOW}${BOLD}⚠️  HINWEIS: Dies ruft GPT-4 auf und kostet ~$0.004${NC}"
echo -e "${YELLOW}Soll der Test ausgeführt werden? (y/n)${NC}"
read -r -n 1 answer
echo ""

if [[ $answer =~ ^[Yy]$ ]]; then
    response=$(curl -s -w "\n%{http_code}" -X POST "${API_BASE}/strom/dispatch" \
        -H "Content-Type: application/json" \
        -d "$payload")
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    print_status $http_code
    print_response "$body"
else
    echo -e "${YELLOW}${BOLT} Test übersprungen${NC}"
fi

# ═══════════════════════════════════════════════════════════════════
# TEST 9: KALIBRIERUNG/TOPICS (PUT) - DRY RUN
# ═══════════════════════════════════════════════════════════════════

print_section "${BOOK} TEST 9: TOPICS HINZUFÜGEN (PUT)"

print_test "Neues Topic zur Kategorie 'technologie' hinzufügen"
print_method "PUT"
print_endpoint "/kalibrierung/topics"
print_beschreibung "Fügt 'Blockchain 2.0' zu technologie Topics hinzu (Aktion: add)"

payload='{
  "kategorie": "technologie",
  "topics": ["Blockchain 2.0"],
  "aktion": "add"
}'

print_payload "$payload"

echo -e "${YELLOW}Soll die Kalibrierung geändert werden? (y/n)${NC}"
read -r -n 1 answer
echo ""

if [[ $answer =~ ^[Yy]$ ]]; then
    response=$(curl -s -w "\n%{http_code}" -X PUT "${API_BASE}/kalibrierung/topics" \
        -H "Content-Type: application/json" \
        -d "$payload")
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    print_status $http_code
    print_response "$body"
else
    echo -e "${YELLOW}${BOLT} Test übersprungen${NC}"
fi

# ═══════════════════════════════════════════════════════════════════
# ZUSAMMENFASSUNG
# ═══════════════════════════════════════════════════════════════════

print_header "${DIAMOND} RESONANZ-PROTOKOLL ABGESCHLOSSEN ${DIAMOND}"

echo -e "${CYAN}Getestete Endpoints:${NC}"
echo -e "  ${CHECK} GET  /strom/status"
echo -e "  ${CHECK} GET  /felder/verfuegbar"
echo -e "  ${CHECK} GET  /kalibrierung/topics"
echo -e "  ${CHECK} GET  /kalibrierung/styles"
echo -e "  ${CHECK} GET  /kalibrierung/openai"
echo -e "  ${CHECK} GET  /kalibrierung/cron"
echo -e "  ${CHECK} GET  /resonanz/parameter"
echo -e "  ${BOLT} POST /strom/dispatch (optional)"
echo -e "  ${BOLT} PUT  /kalibrierung/topics (optional)"

echo -e "\n${GREEN}${BOLD}${WAVE} ALLE FELDER RESONIEREN KOHÄRENT ${WAVE}${NC}\n"

echo -e "${CYAN}Vollständiges Log gespeichert in:${NC} /tmp/syntx_api_test.log"
