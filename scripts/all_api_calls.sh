#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════
#
#   ███████╗██╗   ██╗███╗   ██╗████████╗██╗  ██╗
#   ██╔════╝╚██╗ ██╔╝████╗  ██║╚══██╔══╝╚██╗██╔╝
#   ███████╗ ╚████╔╝ ██╔██╗ ██║   ██║    ╚███╔╝ 
#   ╚════██║  ╚██╔╝  ██║╚██╗██║   ██║    ██╔██╗ 
#   ███████║   ██║   ██║ ╚████║   ██║   ██╔╝ ██╗
#   ╚══════╝   ╚═╝   ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝
#
#   F I E L D   I N S P E C T O R   v2.1
#
#   🌊 RESONANZ · ⚡ FELD · 💎 STROM
#
#   TARGET: dev.syntx-system.com (PRODUCTION)
#
# ═══════════════════════════════════════════════════════════════════════════

# FIXED CONFIGURATION
BASE_URL="https://dev.syntx-system.com/api/strom"
TIMEOUT=15
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
TOTAL_TIME=0

# COLORS
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color

# ═══════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

print_header() {
    echo ""
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${WHITE}  $1${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════════════════════${NC}"
}

print_response_preview() {
    local body="$1"
    local max_lines="${2:-15}"
    
    # Format JSON and show preview
    formatted=$(echo "$body" | jq '.' 2>/dev/null)
    if [ $? -eq 0 ]; then
        line_count=$(echo "$formatted" | wc -l)
        echo "$formatted" | head -n $max_lines | sed 's/^/      /'
        if [ $line_count -gt $max_lines ]; then
            echo -e "      ${GRAY}... (+$((line_count - max_lines)) more lines)${NC}"
        fi
    else
        echo "$body" | head -n 5 | sed 's/^/      /'
    fi
}

test_endpoint() {
test_endpoint() {
    local method="$1"
    local path="$2"
    local description="$3"
    local data="$4"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    local url="${BASE_URL}${path}"
    local start_time=$(date +%s%3N)
    
    # Execute request
    if [ "$method" == "GET" ]; then
        HTTP_RESPONSE=$(curl -s -w "\n%{http_code}" --max-time $TIMEOUT "$url" 2>/dev/null)
    elif [ "$method" == "PUT" ] && [ -n "$data" ]; then
        HTTP_RESPONSE=$(curl -s -w "\n%{http_code}" --max-time $TIMEOUT -X PUT -H "Content-Type: application/json" -d "$data" "$url" 2>/dev/null)
    elif [ "$method" == "POST" ] && [ -n "$data" ]; then
        HTTP_RESPONSE=$(curl -s -w "\n%{http_code}" --max-time $TIMEOUT -X POST -H "Content-Type: application/json" -d "$data" "$url" 2>/dev/null)
    elif [ "$method" == "POST" ]; then
        HTTP_RESPONSE=$(curl -s -w "\n%{http_code}" --max-time $TIMEOUT -X POST "$url" 2>/dev/null)
    else
        HTTP_RESPONSE=$(curl -s -w "\n%{http_code}" --max-time $TIMEOUT -X "$method" "$url" 2>/dev/null)
    fi
    
    local end_time=$(date +%s%3N)
    local duration=$((end_time - start_time))
    TOTAL_TIME=$((TOTAL_TIME + duration))
    
    # Split response and status
    HTTP_STATUS=$(echo "$HTTP_RESPONSE" | tail -n 1)
    HTTP_BODY=$(echo "$HTTP_RESPONSE" | sed '$d')
    
    echo ""
    
    # Check status
    if [[ "$HTTP_STATUS" =~ ^2 ]]; then
        PASSED_TESTS=$((PASSED_TESTS + 1))
        
        echo -e "${GREEN}┌──────────────────────────────────────────────────────────────────────────┐${NC}"
        echo -e "${GREEN}│${NC} ${WHITE}✅ ${method} ${path}${NC}"
        echo -e "${GREEN}│${NC} ${GRAY}${description}${NC}"
        echo -e "${GREEN}├──────────────────────────────────────────────────────────────────────────┤${NC}"
        echo -e "${GREEN}│${NC} Status: ${GREEN}${HTTP_STATUS} OK${NC}  |  Time: ${CYAN}${duration}ms${NC}  |  Size: ${BLUE}$(echo "$HTTP_BODY" | wc -c) bytes${NC}"
        echo -e "${GREEN}├──────────────────────────────────────────────────────────────────────────┤${NC}"
        
        # Show keys
        local keys=$(echo "$HTTP_BODY" | jq -r 'keys | join(", ")' 2>/dev/null)
        if [ -n "$keys" ] && [ "$keys" != "null" ]; then
            echo -e "${GREEN}│${NC} ${YELLOW}Keys:${NC} ${keys}"
            echo -e "${GREEN}├──────────────────────────────────────────────────────────────────────────┤${NC}"
        fi
        
        # Show response preview
        echo -e "${GREEN}│${NC} ${YELLOW}Response:${NC}"
        print_response_preview "$HTTP_BODY" 12
        echo -e "${GREEN}└──────────────────────────────────────────────────────────────────────────┘${NC}"
        
    else
        FAILED_TESTS=$((FAILED_TESTS + 1))
        
        echo -e "${RED}┌──────────────────────────────────────────────────────────────────────────┐${NC}"
        echo -e "${RED}│${NC} ${WHITE}❌ ${method} ${path}${NC}"
        echo -e "${RED}│${NC} ${GRAY}${description}${NC}"
        echo -e "${RED}├──────────────────────────────────────────────────────────────────────────┤${NC}"
        echo -e "${RED}│${NC} Status: ${RED}${HTTP_STATUS} FAILED${NC}  |  Time: ${duration}ms"
        echo -e "${RED}├──────────────────────────────────────────────────────────────────────────┤${NC}"
        
        # Show error
        local error_msg=$(echo "$HTTP_BODY" | jq -r '.detail // .message // .error // "Unknown error"' 2>/dev/null)
        echo -e "${RED}│${NC} ${RED}Error:${NC} ${error_msg}"
        echo -e "${RED}└──────────────────────────────────────────────────────────────────────────┘${NC}"
    fi
}
    local method="$1"
    local path="$2"
    local description="$3"
    local data="$4"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    local url="${BASE_URL}${path}"
    local start_time=$(date +%s%3N)
    
    # Execute request
    if [ "$method" == "GET" ]; then
        HTTP_RESPONSE=$(curl -s -w "\n%{http_code}" --max-time $TIMEOUT "$url" 2>/dev/null)
    elif [ "$method" == "POST" ] && [ -n "$data" ]; then
        HTTP_RESPONSE=$(curl -s -w "\n%{http_code}" --max-time $TIMEOUT -X POST -H "Content-Type: application/json" -d "$data" "$url" 2>/dev/null)
    elif [ "$method" == "POST" ]; then
        HTTP_RESPONSE=$(curl -s -w "\n%{http_code}" --max-time $TIMEOUT -X POST "$url" 2>/dev/null)
    else
        HTTP_RESPONSE=$(curl -s -w "\n%{http_code}" --max-time $TIMEOUT -X "$method" "$url" 2>/dev/null)
    fi
    
    local end_time=$(date +%s%3N)
    local duration=$((end_time - start_time))
    TOTAL_TIME=$((TOTAL_TIME + duration))
    
    # Split response and status
    HTTP_STATUS=$(echo "$HTTP_RESPONSE" | tail -n 1)
    HTTP_BODY=$(echo "$HTTP_RESPONSE" | sed '$d')
    
    echo ""
    
    # Check status
    if [[ "$HTTP_STATUS" =~ ^2 ]]; then
        PASSED_TESTS=$((PASSED_TESTS + 1))
        
        echo -e "${GREEN}┌──────────────────────────────────────────────────────────────────────────┐${NC}"
        echo -e "${GREEN}│${NC} ${WHITE}✅ ${method} ${path}${NC}"
        echo -e "${GREEN}│${NC} ${GRAY}${description}${NC}"
        echo -e "${GREEN}├──────────────────────────────────────────────────────────────────────────┤${NC}"
        echo -e "${GREEN}│${NC} Status: ${GREEN}${HTTP_STATUS} OK${NC}  |  Time: ${CYAN}${duration}ms${NC}  |  Size: ${BLUE}$(echo "$HTTP_BODY" | wc -c) bytes${NC}"
        echo -e "${GREEN}├──────────────────────────────────────────────────────────────────────────┤${NC}"
        
        # Show keys
        local keys=$(echo "$HTTP_BODY" | jq -r 'keys | join(", ")' 2>/dev/null)
        if [ -n "$keys" ] && [ "$keys" != "null" ]; then
            echo -e "${GREEN}│${NC} ${YELLOW}Keys:${NC} ${keys}"
            echo -e "${GREEN}├──────────────────────────────────────────────────────────────────────────┤${NC}"
        fi
        
        # Show response preview
        echo -e "${GREEN}│${NC} ${YELLOW}Response:${NC}"
        print_response_preview "$HTTP_BODY" 12
        echo -e "${GREEN}└──────────────────────────────────────────────────────────────────────────┘${NC}"
        
    else
        FAILED_TESTS=$((FAILED_TESTS + 1))
        
        echo -e "${RED}┌──────────────────────────────────────────────────────────────────────────┐${NC}"
        echo -e "${RED}│${NC} ${WHITE}❌ ${method} ${path}${NC}"
        echo -e "${RED}│${NC} ${GRAY}${description}${NC}"
        echo -e "${RED}├──────────────────────────────────────────────────────────────────────────┤${NC}"
        echo -e "${RED}│${NC} Status: ${RED}${HTTP_STATUS} FAILED${NC}  |  Time: ${duration}ms"
        echo -e "${RED}├──────────────────────────────────────────────────────────────────────────┤${NC}"
        
        # Show error
        local error_msg=$(echo "$HTTP_BODY" | jq -r '.detail // .message // .error // "Unknown error"' 2>/dev/null)
        echo -e "${RED}│${NC} ${RED}Error:${NC} ${error_msg}"
        echo -e "${RED}└──────────────────────────────────────────────────────────────────────────┘${NC}"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════
# START INSPECTION
# ═══════════════════════════════════════════════════════════════════════════

clear
echo -e "${PURPLE}"
cat << 'BANNER'

   ███████╗██╗   ██╗███╗   ██╗████████╗██╗  ██╗
   ██╔════╝╚██╗ ██╔╝████╗  ██║╚══██╔══╝╚██╗██╔╝
   ███████╗ ╚████╔╝ ██╔██╗ ██║   ██║    ╚███╔╝ 
   ╚════██║  ╚██╔╝  ██║╚██╗██║   ██║    ██╔██╗ 
   ███████║   ██║   ██║ ╚████║   ██║   ██╔╝ ██╗
   ╚══════╝   ╚═╝   ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝

   F I E L D   I N S P E C T O R   v2.1
   
   🌊 RESONANZ · ⚡ FELD · 💎 STROM
   
BANNER
echo -e "${NC}"

echo -e "${WHITE}═══════════════════════════════════════════════════════════════════════════${NC}"
echo -e "${WHITE}  TARGET:${NC}     ${CYAN}${BASE_URL}${NC}"
echo -e "${WHITE}  TIMESTAMP:${NC}  ${CYAN}$(date '+%Y-%m-%d %H:%M:%S %Z')${NC}"
echo -e "${WHITE}  TIMEOUT:${NC}    ${CYAN}${TIMEOUT}s${NC}"
echo -e "${WHITE}═══════════════════════════════════════════════════════════════════════════${NC}"

# ═══════════════════════════════════════════════════════════════════════════
# HEALTH & SYSTEM
# ═══════════════════════════════════════════════════════════════════════════

print_header "🏥 HEALTH & SYSTEM (3 Endpoints)"

test_endpoint "GET" "/health" "Root Health Check - API Version & Module Status"
test_endpoint "GET" "/health" "Strom Health - Stream Service Status"

# ═══════════════════════════════════════════════════════════════════════════
# FORMATS API (NEU!)
# ═══════════════════════════════════════════════════════════════════════════

print_header "📋 FORMATS API - Dynamic Format Registry (9 Endpoints)"

test_endpoint "GET" "/formats/" "Liste aller verfügbaren Format-Definitionen"
test_endpoint "GET" "/formats/syntex_system" "Format: SYNTEX_SYSTEM vollständig (3 Felder)"
test_endpoint "GET" "/formats/syntex_system/fields" "Feld-Definitionen für Scorer (DE)"
test_endpoint "GET" "/formats/syntex_system/fields?language=en" "Feld-Definitionen für Scorer (EN)"
test_endpoint "GET" "/formats/syntex_system/summary" "Format Summary - Kurzübersicht"
test_endpoint "GET" "/formats/human" "Format: HUMAN (6 Felder für menschliche Analyse)"
test_endpoint "GET" "/formats/sigma" "Format: SIGMA (6 Felder für Signal-Analyse)"
test_endpoint "POST" "/formats/validate" "Format Validierung ohne Speichern" '{"name":"test","fields":[{"name":"a","description":"test","weight":100}]}'
test_endpoint "POST" "/formats/clear-cache" "LRU Cache leeren für Format-Reload"

# ═══════════════════════════════════════════════════════════════════════════
# ANALYTICS
# ═══════════════════════════════════════════════════════════════════════════

print_header "📊 ANALYTICS (7 Endpoints)"

test_endpoint "GET" "/analytics/complete-dashboard" "Complete Dashboard - Full System Overview"
test_endpoint "GET" "/analytics/topics" "Topics Analysis - Themen-Verteilung"
test_endpoint "GET" "/analytics/trends" "Trends - Score-Entwicklung & Predictions"
test_endpoint "GET" "/analytics/performance" "Performance Metrics - By Wrapper & Bottlenecks"
test_endpoint "GET" "/analytics/scores/distribution" "Score Distribution - Histogram & Statistics"
test_endpoint "GET" "/analytics/success-rate" "Success Rate - Gesamt-Erfolgsquote"
test_endpoint "GET" "/analytics/success-rate/by-wrapper" "Success Rate by Wrapper - Pro Wrapper"

# ═══════════════════════════════════════════════════════════════════════════
# EVOLUTION & COMPARE
# ═══════════════════════════════════════════════════════════════════════════

print_header "🔬 EVOLUTION & COMPARE (2 Endpoints)"

test_endpoint "GET" "/evolution/syntx-vs-normal" "SYNTX vs Normal - Paradigm Comparison"
test_endpoint "GET" "/compare/wrappers" "Wrapper Comparison - All Wrappers Side-by-Side"

# ═══════════════════════════════════════════════════════════════════════════
# FELD & STROM
# ═══════════════════════════════════════════════════════════════════════════

print_header "🌊 FELD & STROM (4 Endpoints)"

test_endpoint "GET" "/feld/drift" "Drift Analysis - Driftkörper Detection"
test_endpoint "GET" "/feld/topics" "Feld Topics - Topic Counts"
test_endpoint "GET" "/feld/prompts" "Feld Prompts - Unique Prompt Stats"
test_endpoint "GET" "/generation/progress" "Generation Progress - Trend & Verbesserung"

# ═══════════════════════════════════════════════════════════════════════════
# PROMPTS
# ═══════════════════════════════════════════════════════════════════════════

print_header "📝 PROMPTS (4 Endpoints)"

test_endpoint "GET" "/prompts/table-view" "Table View - Filterable Prompt Table"
test_endpoint "GET" "/prompts/costs/total" "Total Costs - USD, Tokens, Avg per Prompt"
test_endpoint "GET" "/prompts/complete-export?page=1&page_size=2" "Complete Export - Paginated Full Data"
test_endpoint "GET" "/prompts/complete-export?page=1&page_size=1&min_score=80" "Export with Filter - min_score=80"

# ═══════════════════════════════════════════════════════════════════════════
# MONITORING
# ═══════════════════════════════════════════════════════════════════════════

print_header "👁️ MONITORING (1 Endpoint)"

test_endpoint "GET" "/monitoring/live-queue" "Live Queue Monitor - Real-time Processing Status"

# ═══════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════
# TOPIC WEIGHTS
# ═══════════════════════════════════════════════════════════════════════════

print_header "⚖️ TOPIC WEIGHTS - Persistent Priority Management (4 Endpoints)"

test_endpoint "GET" "/topic-weights" "Get All Topic Weights - Bulk Retrieval"
test_endpoint "PUT" "/topic-weights" "Set All Topic Weights - Bulk Update" '{"weights":{"Quantencomputer":0.9,"KI":0.85}}'
test_endpoint "GET" "/topic-weights/Quantencomputer" "Get Single Topic Weight - Individual Retrieval"
test_endpoint "PUT" "/topic-weights/KI" "Set Single Topic Weight - Individual Update" '{"weight":0.92}'

# ═══════════════════════════════════════════════════════════════════════════
# KRONTUN - Cron Orchestration
# ═══════════════════════════════════════════════════════════════════════════

print_header "🌀 KRONTUN - Advanced Cron Orchestration & Analytics (6 Endpoints)"

test_endpoint "GET" "/kalibrierung/cron/stats" "Live Cron Stats - Real-time Status Dashboard"
test_endpoint "GET" "/kalibrierung/cron/logs?limit=5" "Cron Execution Logs - History with Limit"
test_endpoint "GET" "/kalibrierung/cron/impact" "Cron Impact Analytics - Topics x Time Heatmap"
test_endpoint "GET" "/kalibrierung/cron/test-morning-batch" "Get Cron Details - Individual Cron Info"
test_endpoint "PUT" "/kalibrierung/cron/test-cron-update" "Update Cron Config - Modify Zeit/Felder" '{"zeit":"06:00","felder":{"KI":0.9}}'
test_endpoint "POST" "/kalibrierung/cron/test-cron-trigger/run" "Manual Cron Trigger - Force Execution"

# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo ""
echo -e "${PURPLE}╔═════════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║${NC}                                                                             ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}   ${WHITE}📊 SYNTX FIELD INSPECTION SUMMARY${NC}                                        ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}                                                                             ${PURPLE}║${NC}"
echo -e "${PURPLE}╠═════════════════════════════════════════════════════════════════════════════╣${NC}"
echo -e "${PURPLE}║${NC}                                                                             ${PURPLE}║${NC}"

PASS_RATE=$(echo "scale=1; $PASSED_TESTS * 100 / $TOTAL_TESTS" | bc)
AVG_TIME=$(echo "scale=0; $TOTAL_TIME / $TOTAL_TESTS" | bc)

printf "${PURPLE}║${NC}   ${WHITE}%-20s${NC} ${CYAN}%-10s${NC}                                       ${PURPLE}║${NC}\n" "Total Tests:" "$TOTAL_TESTS (incl. 10 new KRONTUN/Weights)"
printf "${PURPLE}║${NC}   ${GREEN}%-20s${NC} ${GREEN}%-10s${NC}                                       ${PURPLE}║${NC}\n" "Passed:" "$PASSED_TESTS"
printf "${PURPLE}║${NC}   ${RED}%-20s${NC} ${RED}%-10s${NC}                                       ${PURPLE}║${NC}\n" "Failed:" "$FAILED_TESTS"
printf "${PURPLE}║${NC}   ${WHITE}%-20s${NC} ${CYAN}%-10s${NC}                                       ${PURPLE}║${NC}\n" "Pass Rate:" "${PASS_RATE}%"
printf "${PURPLE}║${NC}   ${WHITE}%-20s${NC} ${CYAN}%-10s${NC}                                       ${PURPLE}║${NC}\n" "Total Time:" "${TOTAL_TIME}ms"
printf "${PURPLE}║${NC}   ${WHITE}%-20s${NC} ${CYAN}%-10s${NC}                                       ${PURPLE}║${NC}\n" "Avg Response:" "${AVG_TIME}ms"

echo -e "${PURPLE}║${NC}                                                                             ${PURPLE}║${NC}"
echo -e "${PURPLE}╠═════════════════════════════════════════════════════════════════════════════╣${NC}"
echo -e "${PURPLE}║${NC}                                                                             ${PURPLE}║${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${PURPLE}║${NC}   ${GREEN}╔═══════════════════════════════════════════════════════════════════╗${NC}   ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}   ${GREEN}║                                                                   ║${NC}   ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}   ${GREEN}║     🌊 ALL FIELDS RESONATING PERFECTLY! 💎  100% PASS RATE       ║${NC}   ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}   ${GREEN}║                                                                   ║${NC}   ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}   ${GREEN}╚═══════════════════════════════════════════════════════════════════╝${NC}   ${PURPLE}║${NC}"
else
    echo -e "${PURPLE}║${NC}   ${YELLOW}╔═══════════════════════════════════════════════════════════════════╗${NC}   ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}   ${YELLOW}║                                                                   ║${NC}   ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}   ${YELLOW}║     ⚠️  SOME FIELDS NEED CALIBRATION - CHECK FAILED ENDPOINTS     ║${NC}   ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}   ${YELLOW}║                                                                   ║${NC}   ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}   ${YELLOW}╚═══════════════════════════════════════════════════════════════════╝${NC}   ${PURPLE}║${NC}"
fi

echo -e "${PURPLE}║${NC}                                                                             ${PURPLE}║${NC}"
echo -e "${PURPLE}╠═════════════════════════════════════════════════════════════════════════════╣${NC}"
echo -e "${PURPLE}║${NC}                                                                             ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}   ${WHITE}Endpoint Categories:${NC}                                                     ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}   ${GRAY}• Health & System:     2 endpoints${NC}                                       ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}   ${GRAY}• Formats API:         9 endpoints (Dynamic Format Registry)${NC}             ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}   ${GRAY}• Analytics:           7 endpoints${NC}                                       ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}   ${GRAY}• Evolution & Compare: 2 endpoints${NC}                                       ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}   ${GRAY}• Feld & Strom:        4 endpoints${NC}                                       ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}   ${GRAY}• Prompts:             4 endpoints${NC}                                       ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}   ${GRAY}• Monitoring:          1 endpoint${NC}                                        ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}   ${GRAY}• Topic Weights:       4 endpoints (Persistent Priority Control)${NC}        ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}   ${GRAY}• KRONTUN:             6 endpoints (Cron Orchestration & Analytics)${NC}     ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}                                                                             ${PURPLE}║${NC}"
echo -e "${PURPLE}╚═════════════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${PURPLE}═══════════════════════════════════════════════════════════════════════════${NC}"
echo -e "${WHITE}  🌊 SYNTX FIELD INSPECTOR v2.1 · ${CYAN}${BASE_URL}${NC} · ${WHITE}⚡💎${NC}"
echo -e "${PURPLE}═══════════════════════════════════════════════════════════════════════════${NC}"
echo ""

exit $FAILED_TESTS
