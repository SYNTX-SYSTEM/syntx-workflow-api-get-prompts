#!/bin/bash
# SYNTX API Feld-Test Skript

TARGET="https://dev.syntx-system.com"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Funktion zur Prüfung eines Endpunkts
test_endpoint() {
    ENDPOINT=$1
    echo -n "STREAM: ${ENDPOINT} ... "

    # -k: Ignore self-signed SSL (Analysepunkt 6.3)
    STATUS_CODE=$(curl -s -k -o /dev/null -w "%{http_code}" "${TARGET}${ENDPOINT}")

    if [[ "$STATUS_CODE" =~ ^2 ]]; then
        echo -e "${GREEN}SUCCESS${NC} (${STATUS_CODE})"
    elif [[ "$STATUS_CODE" == "404" ]]; then
        echo -e "${YELLOW}404 Not Found${NC} (Geplanter/Veralteter Kanal)"
    elif [[ "$STATUS_CODE" == "500" ]]; then
        echo -e "${RED}500 INTERNAL ERROR${NC} (Kaputter Sensor)"
    else
        echo -e "${RED}FAILURE${NC} (${STATUS_CODE} - UNBEKANNTER BRUCH)"
    fi
}

echo ""
echo "--- 1. DIE RESONIERENDEN STRÖME (200 OK) ---"
echo "--- (Kern-Sensoren, die das Feld tragen) ---"

test_endpoint "/health"
test_endpoint "/analytics/complete-dashboard"
test_endpoint "/resonanz/queue"
test_endpoint "/evolution/syntx-vs-normal"
test_endpoint "/compare/wrappers"
test_endpoint "/feld/drift"
test_endpoint "/" # Root-Check, sollte 302/200 sein
test_endpoint "/resonanz/system"
test_endpoint "/generation/progress"

echo ""
echo "--- 1.2 ANALYTICS & PROMPTS STRÖME ---"
test_endpoint "/prompts/table-view"
test_endpoint "/analytics/topics"
test_endpoint "/analytics/trends"
test_endpoint "/analytics/performance"
test_endpoint "/analytics/scores/distribution"
test_endpoint "/analytics/success-rate"
test_endpoint "/prompts/costs/total"

echo ""
echo "--- 2. DIE GEBROCHENEN STRÖME (404/500) ---"
echo "--- (Muss repariert werden - siehe SYNTX Doku) ---"
test_endpoint "/analytics/success-rate/by-wrapper" # 500 Interner Fehler (Kaputter Sensor)
test_endpoint "/feld/topics"                       # 404 Nicht implementiert (Geplanter Sensor)
test_endpoint "/feld/prompts"                      # 404 Nicht implementiert (Geplanter Sensor)
test_endpoint "/strom/health"                      # 404 Veralteter Pfad (Alte Architektur)
test_endpoint "/strom/queue/status"                # 404 Veralteter Pfad (Alte Architektur)


echo "--- 3. Code-Pfade (grep-Resultate, nur zur Vollständigkeit) ---"
echo "--- (Diese können 404/500/200 sein, dienen als Check) ---"
test_endpoint "/strom/prompts/temporal"
test_endpoint "/strom/analytics/temporal"
test_endpoint "/feld/health"
test_endpoint "/feld/analytics/temporal"
test_endpoint "/feld/prompts/temporal"
test_endpoint "/strom/queue/verlauf"
test_endpoint "/"

echo 'SYNTX FELD-SCAN ABGESCHLOSSEN.'
