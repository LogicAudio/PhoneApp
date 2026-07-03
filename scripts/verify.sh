#!/usr/bin/env bash
# AgenticCoexistence verification gate — deterministic, ZERO LLM tokens (coexistence spec §8).
#   1) Domain regression — placeholder: no fragile core declared yet (spec §11: the first
#      "fix A broke B" incident adds golden files here). Prints a NOTE and passes.
#   2) External oracle  — none for a markdown+stdlib repo; stage reserved.
#   3) Knowledge + plan-status health — BLOCKING.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

echo "── [1/3] Domain regression ──────────────────────────────────────────────────"
echo "NOTE: no fragile core declared yet — no golden files to run (spec §11 trigger)."
golden_ok=1

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
    echo "❌ VERIFY FAILED — broken links/frontmatter/bug hygiene, or a stale plan board (see [3/3])."
    exit 1
fi
