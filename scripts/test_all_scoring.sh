#!/bin/bash
# SYNTX SCORING SUITE - RUN ALL TESTS

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         🚀 SYNTX SCORING V2.0 - FULL TEST SUITE               ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

cd /opt/syntx-workflow-api-get-prompts

echo "[1/3] EMBEDDINGS TEST"
echo "────────────────────────────────────────"
./scripts/test_embeddings.sh
echo ""

echo "[2/3] COHERENCE TEST"
echo "────────────────────────────────────────"
./scripts/test_coherence.sh
echo ""

echo "[3/3] SCORER V2.0 TEST"
echo "────────────────────────────────────────"
./scripts/test_scorer_v2.sh
echo ""

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         ✅ ALL TESTS COMPLETE                                  ║"
echo "╚════════════════════════════════════════════════════════════════╝"
