---
status: done
---

# Plan 01 — Bootstrap de la structure agentique (spec de coexistence §10)

> **Origin (2026-07-03) :** Thomas — « alright I've added instruction on how to maintain this
> project, read Knowledge/agentic-human-coexistence.md » puis « vas y ». Interview §10.1 validée
> sur les propositions de l'agent ; brouillon approuvé en totalité, avec migration
> d'`apps/eatwise/CLAUDE.md` vers `Knowledge/` + fichier pointeur.

## Context

Le repo adopte la structure humain+agent de la spec
[agentic-human-coexistence.md](../Knowledge/agentic-human-coexistence.md) (spec_version 1,
copiée depuis son repo canonique `~/LogicAudio/AgenticCoexistence`). Les moteurs de gate sont
copiés byte-identiques depuis ce repo ; les données propres à PhoneApp (signaux périmés, goldens)
partent de zéro.

## Current state (verified by exploration)

Monorepo Capacitor, 1 app (eatwise, PWA GitHub Pages prioritaire, APK secondaire). Doc existante
avant bootstrap : `CLAUDE.md` racine (carte informelle, 37 lignes), `apps/eatwise/CLAUDE.md`
(règles normatives riches, 141 lignes, en français), `README.md` (mirroir partiel de la carte),
`docs/SETUP.md` (runbook toolchain). Aucun gate déterministe, `core.hooksPath` non configuré,
aucun test. Cœur fragile identifié : `apps/eatwise/www/index.html` (compat du modèle de données
`localStorage`, fenêtre 4h ballonnements, corrélation douleurs J-1/J-2, triple forme
d'`applyImport()`).

## P01.1 — Carte `CLAUDE.md` au squelette §3 · SAFE · low · ✅ DONE (commit 1e322e5)

Invariants read-me-first, cœur fragile déclaré, carte du repo, index Knowledge, légende d'origine,
gotchas, commandes, `spec_version 1`.

## P01.2 — Routeur `AGENTS.md` · SAFE · low · ✅ DONE (commit 80f8683)

Template §3 paramétré.

## P01.3 — `README.md` porte d'entrée · SAFE · low · ✅ DONE (commit 8fc33c1)

≤25 lignes, bloc pointeur vers la carte, suppression du tableau layout (mirroir), URL de prod
PWA conservée.

## P01.4 — Migration docs → `Knowledge/` + seeds · SAFE · medium · ✅ DONE (commit 5bf337b)

`git mv docs/SETUP.md → Knowledge/setup.md` (runbook) ; `git mv apps/eatwise/CLAUDE.md →
Knowledge/eatwise.md` (rules, `governs: apps/eatwise/`, corps verbatim) avec pointeur laissé sur
place ; seeds `conventions.md` + `runbook.md` avec frontmatter §4.

## P01.5 — `Plans/` · SAFE · low · ✅ DONE (commit ae2f677)

Ce plan + `README.md` stub (sentinelles seules, boards générés en P01.7) + `CHANGELOG.md` vide.

## P01.6 — `Bugs/` · SAFE · low · ✅ DONE (commit 99c6cef)

`README.md` (table des bugs ouverts + légende sévérité) + `Solved/.gitkeep`.

## P01.7 — `scripts/` : gates déterministes · SAFE · low · ✅ DONE (commit c75e413)

Copie byte-identique depuis le repo canonique : `check_knowledge.py`, `check_plans.py`,
`verify.sh`, `hooks/pre-commit`, `bootstrap.sh` (vérifiée par `diff`). Fichier
`Knowledge/_meta/stale_signals.txt` créé avec les deux termes retirés par la migration
(`docs/SETUP.md`, `apps/eatwise/CLAUDE.md`). `git config core.hooksPath scripts/hooks` +
génération des boards.

## P01.8 — Goldens du cœur fragile (eatwise) · SAFE (zéro changement de comportement) · medium · ✅ DONE (commit 2bfd359)

Jeu d'entrées figé (`scripts/goldens/eatwise_fixture.json`, résultats vérifiés à la main :
bornes 240/241 min, sev<2 ignoré, seuil 3 jours, delta Gluten +4) + runner node
(`scripts/eatwise_golden.mjs`) qui évalue le script d'`index.html` en sandbox `node:vm` et fige
`normFood`/`tagsFromMeal`, `computeBloat`, `computePain` (champ `days` exclu — dépend du jour
courant), `applyImport` (6 cas), `renderAnalysis`, `buildExport` (`todayISO` figé) contre
`scripts/goldens/eatwise.json`. Branché en stage 1 (BLOCKING) de `verify.sh` ; le pre-commit
bloque quand `apps/eatwise/www/index.html` est stagé et que les goldens échouent — testé en
cassant volontairement le seuil de `computePain()` (goldens rouges, commit refusé), puis revert.
Mise à jour d'une baseline = délibérée, avec accord explicite de Thomas
(`node scripts/eatwise_golden.mjs --update`).

## Verification

- Les deux checkers exit 0 ; `--strict` sans orphelin.
- `scripts/verify.sh` vert de bout en bout, stage 1 = goldens réels (plus de placeholder).
- Altérer volontairement `computePain()` fait échouer les goldens (test du gate), puis revert.
- Hooks installés (`git config core.hooksPath` → `scripts/hooks`).
- README ≤25 lignes ; carte ≤400 lignes ; chaque doc Knowledge atteignable depuis l'index.
- Ce plan `done` sur le board généré + ligne CHANGELOG.
