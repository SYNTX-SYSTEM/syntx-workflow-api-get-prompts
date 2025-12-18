#!/bin/bash
# ============================================================================
# SYNTX COHERENCE TEST SCRIPT
# ============================================================================

# Farben
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║${WHITE}        🔗 SYNTX COHERENCE TEST SUITE v2.0                        ${CYAN}║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════╝${NC}"
echo ""

python3 << 'PYTHON'
import sys
sys.path.insert(0, '/opt/syntx-workflow-api-get-prompts')

RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
CYAN = '\033[0;36m'
WHITE = '\033[1;37m'
PURPLE = '\033[0;35m'
NC = '\033[0m'

print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
print(f"{WHITE}[1/3] Loading Coherence Analyzer...{NC}")
print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")

try:
    from syntex_injector.syntex.analysis.coherence import (
        analyze_pairwise_coherence, calculate_coherence_score, detect_incoherence
    )
    print(f"{GREEN}✅ Coherence Analyzer loaded{NC}")
except Exception as e:
    print(f"{RED}❌ Import Error: {e}{NC}")
    sys.exit(1)

print("")
print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
print(f"{WHITE}[2/3] Coherence Tests...{NC}")
print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")

# Test 1: Kohärente SYNTX Felder
print(f"\n{PURPLE}═══ TEST 1: Kohärente SYNTX Felder ═══{NC}\n")

coherent_fields = {
    "driftkorper": """
        Die Struktur des Systems zeigt eine hierarchische Organisation.
        Auf TIER-1 sehen wir die sichtbare Oberfläche der Komponenten.
        TIER-2 offenbart die inneren Verbindungen zwischen Modulen.
        Der Kern auf TIER-4 ist ein selbstregulierendes Netzwerk.
    """,
    "kalibrierung": """
        Das System passt sich durch Feedback-Mechanismen an.
        Bei Störungen justiert es automatisch seine Parameter.
        Die Selbstregulation erfolgt über mehrere Ebenen.
        Dynamische Anpassung ist das zentrale Prinzip.
    """,
    "stromung": """
        Informationsflüsse verbinden alle Systemebenen.
        Daten zirkulieren von der Oberfläche zum Kern.
        Energie fließt durch die hierarchischen Strukturen.
        Der Kreislauf erhält das Gleichgewicht aufrecht.
    """
}

result1 = analyze_pairwise_coherence(coherent_fields, "SYNTEX_SYSTEM")

print(f"  {WHITE}Driftkörper:{NC} Hierarchische Systemstruktur...")
print(f"  {WHITE}Kalibrierung:{NC} Feedback und Selbstregulation...")
print(f"  {WHITE}Strömung:{NC} Informationsflüsse und Kreisläufe...")
print("")

for detail in result1["details"]:
    sim = detail["similarity"]
    bar_len = int(sim * 20)
    bar = "█" * bar_len + "░" * (20 - bar_len)
    status = f"{GREEN}✓{NC}" if detail["passed"] else f"{RED}✗{NC}"
    print(f"  {status} {detail['pair']}")
    print(f"    {YELLOW}[{bar}]{NC} {sim:.3f} (min: {detail['min_expected']})")

avg1 = result1["average_coherence"]
print(f"\n  {WHITE}Average Coherence:{NC} {avg1:.3f}")

# Test 2: Inkohärente Felder
print(f"\n{PURPLE}═══ TEST 2: Inkohärente Felder (Random Topics) ═══{NC}\n")

incoherent_fields = {
    "driftkorper": "Pizza ist ein beliebtes italienisches Gericht mit Tomaten und Käse.",
    "kalibrierung": "Der Aktienmarkt reagiert sensibel auf politische Entscheidungen weltweit.",
    "stromung": "Elefanten leben in Afrika und Asien in großen Familienverbänden."
}

result2 = analyze_pairwise_coherence(incoherent_fields, "SYNTEX_SYSTEM")

print(f"  {WHITE}Driftkörper:{NC} Pizza...")
print(f"  {WHITE}Kalibrierung:{NC} Aktienmarkt...")
print(f"  {WHITE}Strömung:{NC} Elefanten...")
print("")

for detail in result2["details"]:
    sim = detail["similarity"]
    bar_len = int(sim * 20)
    bar = "█" * bar_len + "░" * (20 - bar_len)
    status = f"{GREEN}✓{NC}" if detail["passed"] else f"{RED}✗{NC}"
    print(f"  {status} {detail['pair']}")
    print(f"    {YELLOW}[{bar}]{NC} {sim:.3f} (min: {detail['min_expected']})")

avg2 = result2["average_coherence"]
print(f"\n  {WHITE}Average Coherence:{NC} {avg2:.3f}")

# Test 3: Incoherence Detection
print(f"\n{PURPLE}═══ TEST 3: Incoherence Detection ═══{NC}\n")

warnings = detect_incoherence(incoherent_fields, "SYNTEX_SYSTEM")
if warnings:
    print(f"  {YELLOW}⚠️  Detected {len(warnings)} incoherence warning(s):{NC}")
    for w in warnings:
        print(f"    {RED}• {w}{NC}")
else:
    print(f"  {GREEN}No incoherence detected{NC}")

# Summary
print("")
print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
print(f"{WHITE}[3/3] Summary{NC}")
print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
print("")

diff = avg1 - avg2
test_passed = avg1 > avg2 and diff > 0.1

print(f"  {WHITE}Coherent Fields Score:{NC}   {GREEN}{avg1:.3f}{NC}")
print(f"  {WHITE}Incoherent Fields Score:{NC} {RED}{avg2:.3f}{NC}")
print(f"  {WHITE}Difference:{NC}              {YELLOW}{diff:+.3f}{NC}")
print("")

if test_passed:
    print(f"  {GREEN}╔═══════════════════════════════════════════════════╗{NC}")
    print(f"  {GREEN}║  ✅ COHERENCE DETECTION WORKING CORRECTLY        ║{NC}")
    print(f"  {GREEN}║     Coherent > Incoherent by {diff:.3f}                ║{NC}")
    print(f"  {GREEN}╚═══════════════════════════════════════════════════╝{NC}")
else:
    print(f"  {RED}╔═══════════════════════════════════════════════════╗{NC}")
    print(f"  {RED}║  ❌ COHERENCE DETECTION FAILED                    ║{NC}")
    print(f"  {RED}╚═══════════════════════════════════════════════════╝{NC}")

print("")
PYTHON

echo -e "${CYAN}══════════════════════════════════════════════════════════════════${NC}"
echo -e "${WHITE}                    SYNTX COHERENCE TEST COMPLETE                 ${NC}"
echo -e "${CYAN}══════════════════════════════════════════════════════════════════${NC}"
echo ""
