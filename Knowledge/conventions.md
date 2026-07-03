---
name: conventions
type: reference
governs: []
read_when: Naming an app or file, choosing where code lives, committing, or wondering about the stack.
---

# Conventions

Cross-cutting facts that aren't per-app rules. The always-follow invariants live in
[CLAUDE.md](../CLAUDE.md); per-app behaviour lives in the app's rules doc (e.g.
[eatwise.md](eatwise.md)).

## Stack

- Web code: plain HTML/CSS/JS; no framework unless an app's rules doc says otherwise.
- Native wrapper: Capacitor (Android project committed per app; iOS addable later).
- Tooling: npm workspaces + bash scripts in `shared/scripts/`.
- Gates: python3, stdlib only (`scripts/check_*.py`) — engines copied byte-identical from the
  canonical coexistence repo; repo-specific data lives in data files, never in the engines.

## Naming

- App ids: `net.transpose.<name>`; app folders: lowercase, no spaces.
- Knowledge docs: `kebab-case.md`, `name:` equal to the filename stem.
- Plans: `Plans/NN_snake_topic.md`; bugs: `Bugs/NNN_snake_topic.md`.

## Git workflow

- Solo repo: commits land directly on `main`. GitHub Pages deploys EatWise on every push touching
  `apps/eatwise/www/`.
- Commit messages in French; plan work references its item: `Plan NN: <item>`.
- A change to code behaviour updates the governing Knowledge doc **in the same commit** (sync
  rule, coexistence spec §4).
- Renaming or retiring a term adds the old term to `_meta/stale_signals.txt` in the same commit.

## Languages

- Exchanges with Thomas and commit messages: French.
- Repo-level docs (map, router, README, this file): English.
- EatWise: doc, UI and code comments in French (see [eatwise.md](eatwise.md)).
