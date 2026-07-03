# CHANGELOG — milestones

> One line per landed plan. Full history: `git log`. Per-plan status: the auto-generated
> [README.md](README.md) board. This file is the human-readable pulse — milestones only.

## 2026-07-03 — Plan 01 done: bootstrap de la structure agentique (spec_version 1)
Le repo adopte la structure de coexistence humain+agent : carte CLAUDE.md (§3), routeur
AGENTS.md, Knowledge/ avec frontmatter (conventions, runbook, setup, eatwise migrés depuis
docs/ et apps/eatwise/CLAUDE.md), Plans/ + Bugs/, moteurs de gate copiés byte-identiques du
repo canonique AgenticCoexistence, et goldens du cœur fragile EatWise branchés dans verify.sh
et le pre-commit (commits 1e322e5 → 2bfd359).
