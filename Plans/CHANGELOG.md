# CHANGELOG — milestones

> One line per landed plan. Full history: `git log`. Per-plan status: the auto-generated
> [README.md](README.md) board. This file is the human-readable pulse — milestones only.

## 2026-07-03 — Plan 01 done: bootstrap de la structure agentique (spec_version 1)
Le repo adopte la structure de coexistence humain+agent : carte CLAUDE.md (§3), routeur
AGENTS.md, Knowledge/ avec frontmatter (conventions, runbook, setup, eatwise migrés depuis
docs/ et apps/eatwise/CLAUDE.md), Plans/ + Bugs/, moteurs de gate copiés byte-identiques du
repo canonique AgenticCoexistence, et goldens du cœur fragile EatWise branchés dans verify.sh
et le pre-commit (commits 1e322e5 → 2bfd359).

## 2026-07-03 — Plan 02 done: EatWise 3.16.0 (UX analyse + refonte visuelle)
Palette type Gluci-Chek (une couleur par fonction), onglet Données en 2 étapes sans jargon
(« Envoyer mes données à Claude » via claude.ai/new?q= + import tolérant extractJSON), prompt
d'analyse v2 avec miroir réviewable Knowledge/eatwise-prompt.md (golden buildExport recalé sur
demande de Thomas), idées recettes dans la boucle d'analyse, icônes renommées anti-cache WebAPK
(icon-2.svg + PNG 192/512). Déployée et confirmée en production (commit 9bf2573).

## 2026-07-03 — Plan 03 done: EatWise 3.16.1 → 3.17.1 (UI mobile + qualité de vie)
Grille de tuiles colorées façon référence Gluci-Chek et gros boutons (3.16.1) ; carte d'analyse
déplacée dans l'onglet Analyse avec note multi-IA, historique d'analyses datées (champ additif),
bouton « Encore ce repas », storage.persist(), service worker network-first = mises à jour
instantanées (3.17.0) ; prompt recohérencé vers l'onglet Analyse, golden recalé (3.17.1).
Confirmée en production (commit f7c0d19).
