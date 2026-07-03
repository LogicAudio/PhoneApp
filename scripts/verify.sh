#!/usr/bin/env bash
# PhoneApp verification gate — deterministic, ZERO LLM tokens (coexistence spec §8).
#   1) Domain regression — BLOCKING: goldens du cœur fragile EatWise
#      (apps/eatwise/www/index.html), voir scripts/eatwise_golden.mjs.
#   2) External oracle  — none declared; stage reserved.
#   3) Knowledge + plan-status health — BLOCKING.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

echo "── [1/3] Domain regression (goldens EatWise, blocking) ──────────────────────"
golden_ok=1
if command -v node >/dev/null 2>&1; then
    node scripts/eatwise_golden.mjs || golden_ok=0
else
    echo "❌ node introuvable — le gate du cœur fragile ne peut pas tourner (node est requis pour développer ce repo)."
    golden_ok=0
fi

echo ""
echo "── [2/3] External oracle ────────────────────────────────────────────────────"
echo "NOTE: none declared — stage reserved."

echo ""
echo "── [3/3] Knowledge + plan-status health (deterministic, blocking) ───────────"
docs_ok=1
python3 scripts/check_knowledge.py || docs_ok=0
echo ""
python3 scripts/check_plans.py --check || docs_ok=0

echo ""
if [ "$golden_ok" = "1" ] && [ "$docs_ok" = "1" ]; then
    echo "✅ VERIFY PASSED — knowledge/plans healthy."
    exit 0
else
    echo "❌ VERIFY FAILED — golden regression (see [1/3]), or broken links/frontmatter/bug hygiene/stale plan board (see [3/3])."
    exit 1
fi
