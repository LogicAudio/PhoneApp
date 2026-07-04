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

## 2026-07-03 — Plan 04 done: EatWise 3.18.0 → 3.19.0 (Recettes + choix de l'IA)
Onglet Recettes (déjeuner rapide / dîner / souper, prompt chef-nutritionniste FODMAP construit
sur les aliments tolérés/suspects + envies du jour), onglet Analyse réordonné (graphiques →
analyse IA → mise à jour), sélecteur d'IA mémorisé (Claude/ChatGPT pré-remplis via ?q=,
Gemini copie+ouverture, ou copier seulement) avec bouton générique « Analyser mes données ».
Confirmée en production (commit 06e38ce).

## 2026-07-03 — Plan 06 done: EatWise 3.20.0 (sélection Thomas du backlog)
Badge « douleur du jour non notée », édition d'une entrée en place, raideur matinale ×
alimentation (computeStiff, J-1/J-2), graphe 14 jours combiné (douleur + ballonnements +
repas suspects), rapport imprimable pour le rhumatologue. Confirmée en production
(commit 84a2c8c).

## 2026-07-03 — Plan 07 done: EatWise 3.21.0 (rapport médecin v2, standards cliniques)
Rapport refondu sur les référentiels réels (journal aliments-symptômes des diététiciens,
cadrage BASDAI des rhumatologues) : journal 14 jours horodaté avec délais en toutes lettres,
synthèse en indicateurs 0-10, complétude du journal, courbe 28 jours avec axe Y, bouton
Imprimer/PDF, viewport mobile. Graphe in-app : axe Y + marqueurs séparés (échelles
distinctes). Confirmée en production (commit 9f967e3).

## 2026-07-03 — Plan 08 done: EatWise 3.22.0 (analyse sans recettes)
Séparation nette des circuits : le prompt d'analyse (v3) ne demande plus de recettes (point
supprimé, interdiction explicite, titre ## Recettes retiré) — l'onglet Recettes reste le seul
circuit, en lecture directe. Golden recalé sur demande. Confirmée en production (ad0dd5c).

## 2026-07-03 — Plan 09 done: EatWise 3.23.0/3.23.1 (libellés paramétrables + café)
L'app devient multi-maladies : carte « Personnalisation des suivis » (symptôme rapide, suivi
quotidien, case du matin, situation santé — champ additif labels), libellés propagés partout,
prompt v4 avec détection de spécialité (dermatologie/rhumatologie/gastro selon les intitulés),
golden recalé. Bouton « Buy me a coffee » (buymeacoffee.com/logicaudio) au footer et dans
Données. En production (commit 6cecd29) après un incident intermittent GitHub Pages.

## 2026-07-03 — Plan 10 done: EatWise 3.28.0 (associations d'aliments + graphe normalisé)
computeBloatPairs() : paires d'aliments présentes ensemble avant les épisodes (>=2 fois),
affichées dans Analyse et injectées dans le RÉSUMÉ du prompt (consigne « départager les
co-suspects », golden recalé) — l'analyseur maison voulu par Thomas. Ballonnement normalisé
0-10 en barres groupées sur les deux graphes. En production (665f4cc) après une série
d'échecs deploy-pages côté GitHub, résorbés par relances automatiques de la boucle.

## 2026-07-04 — Plan 11 done: EatWise 3.29.0 (presse-papier + point d'analyse)
Bannière « Analyse détectée dans le presse-papier — Enregistrer / Ignorer » au retour dans
l'app (échec de permission silencieux, jamais d'import automatique, jamais re-proposé) et
point sarcelle sur l'onglet Analyse quand l'analyse est périmée (aucune + >=5 entrées, >=10
nouvelles entrées, ou >=14 jours). En production (8265e26).
