#!/usr/bin/env bash
# One-time per-clone setup (coexistence spec §8) — deterministic, ZERO LLM tokens.
set -euo pipefail
cd "$(dirname "$0")/.." || exit 1

echo "── bootstrap: git hooks ─────────────────────────────────────────────────────"
git config core.hooksPath scripts/hooks
echo "core.hooksPath → scripts/hooks (bypass a single commit with: git commit --no-verify)"

if [ -f requirements.txt ]; then
    echo ""
    echo "── bootstrap: python env ────────────────────────────────────────────────────"
    [ -d .venv ] || { python3 -m venv .venv && ./.venv/bin/pip install -q -r requirements.txt; }
fi

echo ""
echo "── bootstrap: rot-guards ────────────────────────────────────────────────────"
python3 scripts/check_knowledge.py
echo ""
python3 scripts/check_plans.py --check

echo ""
echo "✅ bootstrap complete — daily commands live in Knowledge/runbook.md"
