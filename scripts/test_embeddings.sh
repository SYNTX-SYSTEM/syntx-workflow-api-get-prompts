#!/bin/bash
# ============================================================================
# SYNTX EMBEDDINGS TEST SCRIPT
# ============================================================================

# Farben
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Header
echo ""
echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║${WHITE}        🔬 SYNTX EMBEDDINGS TEST SUITE v2.0                      ${PURPLE}║${NC}"
echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Python Test Script
python3 << 'PYTHON'
import sys
sys.path.insert(0, '/opt/syntx-workflow-api-get-prompts')

# Farben für Python
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
CYAN = '\033[0;36m'
WHITE = '\033[1;37m'
NC = '\033[0m'

print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
print(f"{WHITE}[1/4] Loading Embedding Model...{NC}")
print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")

try:
    from syntex_injector.syntex.analysis.embeddings import (
        semantic_similarity, keyword_coverage, _get_model
    )
    model = _get_model()
    if model:
        print(f"{GREEN}✅ Model loaded successfully{NC}")
        print(f"{BLUE}   Model: paraphrase-multilingual-MiniLM-L12-v2{NC}")
    else:
        print(f"{RED}❌ Model failed to load{NC}")
        sys.exit(1)
except Exception as e:
    print(f"{RED}❌ Import Error: {e}{NC}")
    sys.exit(1)

print("")
print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
print(f"{WHITE}[2/4] Semantic Similarity Tests...{NC}")
print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")

# Test Cases
tests = [
    {
        "name": "SYNTX Related (DE)",
        "text1": "Der Driftkörper analysiert die fundamentale Struktur des Systems.",
        "text2": "Die Analyse der Kernstruktur zeigt tiefe Zusammenhänge.",
        "expected": "HIGH",
        "threshold": 0.4
    },
    {
        "name": "SYNTX Unrelated (DE)",
        "text1": "Der Driftkörper analysiert die fundamentale Struktur des Systems.",
        "text2": "Pizza ist ein italienisches Gericht mit Käse.",
        "expected": "LOW",
        "threshold": 0.2
    },
    {
        "name": "Identical Texts",
        "text1": "Kalibrierung der Systemparameter.",
        "text2": "Kalibrierung der Systemparameter.",
        "expected": "PERFECT",
        "threshold": 0.99
    },
    {
        "name": "Semantic Paraphrase",
        "text1": "Das System passt sich dynamisch an.",
        "text2": "Eine dynamische Anpassung des Systems erfolgt.",
        "expected": "HIGH",
        "threshold": 0.5
    },
    {
        "name": "Cross-Language (DE/EN)",
        "text1": "Die Strömung fließt durch das System.",
        "text2": "The flow moves through the system.",
        "expected": "MEDIUM",
        "threshold": 0.3
    }
]

passed = 0
failed = 0

for i, test in enumerate(tests, 1):
    sim = semantic_similarity(test["text1"], test["text2"])
    
    if test["expected"] == "HIGH" and sim >= test["threshold"]:
        status = f"{GREEN}PASS{NC}"
        passed += 1
    elif test["expected"] == "LOW" and sim < test["threshold"]:
        status = f"{GREEN}PASS{NC}"
        passed += 1
    elif test["expected"] == "PERFECT" and sim >= test["threshold"]:
        status = f"{GREEN}PASS{NC}"
        passed += 1
    elif test["expected"] == "MEDIUM" and sim >= test["threshold"]:
        status = f"{GREEN}PASS{NC}"
        passed += 1
    else:
        status = f"{RED}FAIL{NC}"
        failed += 1
    
    # Score Bar
    bar_len = int(sim * 20)
    bar = "█" * bar_len + "░" * (20 - bar_len)
    
    print(f"")
    print(f"  {WHITE}Test {i}: {test['name']}{NC}")
    print(f"  {BLUE}Text 1:{NC} {test['text1'][:50]}...")
    print(f"  {BLUE}Text 2:{NC} {test['text2'][:50]}...")
    print(f"  {YELLOW}Score:{NC}  [{bar}] {sim:.3f}")
    print(f"  {WHITE}Expected:{NC} {test['expected']} | {WHITE}Result:{NC} {status}")

print("")
print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
print(f"{WHITE}[3/4] Keyword Coverage Tests...{NC}")
print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")

text = "Die Struktur zeigt eine klare Hierarchie mit Kern und Mechanismus."
keywords = ["struktur", "kern", "mechanismus", "hierarchie", "pizza"]

coverage = keyword_coverage(text, keywords)
found = sum(1 for kw in keywords if kw.lower() in text.lower())

print(f"")
print(f"  {WHITE}Text:{NC} {text}")
print(f"  {WHITE}Keywords:{NC} {keywords}")
print(f"  {YELLOW}Coverage:{NC} {found}/{len(keywords)} = {coverage:.1%}")

for kw in keywords:
    if kw.lower() in text.lower():
        print(f"    {GREEN}✓{NC} {kw}")
    else:
        print(f"    {RED}✗{NC} {kw}")

print("")
print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
print(f"{WHITE}[4/4] Summary{NC}")
print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
print("")

total = passed + failed
if failed == 0:
    print(f"  {GREEN}╔═══════════════════════════════════════╗{NC}")
    print(f"  {GREEN}║  ✅ ALL TESTS PASSED ({passed}/{total})            ║{NC}")
    print(f"  {GREEN}╚═══════════════════════════════════════╝{NC}")
else:
    print(f"  {RED}╔═══════════════════════════════════════╗{NC}")
    print(f"  {RED}║  ⚠️  {failed} TEST(S) FAILED ({passed}/{total})          ║{NC}")
    print(f"  {RED}╚═══════════════════════════════════════╝{NC}")

print("")
PYTHON

echo -e "${PURPLE}══════════════════════════════════════════════════════════════════${NC}"
echo -e "${WHITE}                    SYNTX EMBEDDINGS TEST COMPLETE                ${NC}"
echo -e "${PURPLE}══════════════════════════════════════════════════════════════════${NC}"
echo ""
