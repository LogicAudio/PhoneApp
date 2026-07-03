---
status: in-progress
priority: now
---

# Plan 04 — Onglet Recettes + réorganisation de l'onglet Analyse

> **Origin (2026-07-03) :** Thomas — « Dans l'onglet analyse mets dabord tes grapiccs ensuite
> l'analyse IA ensuite l'update button. Peut etre un nouvel onglet pour les recettes, genre
> obtenir mes recettes pour aujourd'hui, dejeuner (rapide) diner, souper sur base de mon
> analyse (extraction d'analyse et renvoi sur claude) ».

## Context

MINOR 3.18.0. Vocabulaire belge assumé : déjeuner = matin (rapide), dîner = midi, souper =
soir. Le prompt recettes est un second prompt, distinct de `buildExport()` (qui reste
golden-figé) — documenté lui aussi dans le miroir `Knowledge/eatwise-prompt.md`.

## P04.1 — Ordre de l'onglet Analyse · SAFE · low · ✅ DONE (3.18.0)

Graphiques/statistiques d'abord (Ballonnements, Douleurs), puis la carte « Analyse IA »,
puis le bouton de mise à jour, puis les analyses précédentes.

## P04.2 — Onglet Recettes · SAFE · medium · ✅ DONE (3.18.0)

Nouvel onglet : champ « envies/contraintes du jour » (optionnel) + trois boutons
(🥐 Déjeuner rapide, 🍽 Dîner, 🍲 Souper). Chaque bouton construit `buildRecipePrompt(kind)` :
chef-nutritionniste FODMAP/inflammation, 3 idées, aliments bien tolérés (taux ballonnements
≤ 20 %) vs suspects (≥ 50 % ou douleur +1), dernière analyse incluse, envies du jour —
puis copie + ouverture de Claude (`?q=`, le prompt recettes tient largement dans l'URL),
collable dans n'importe quelle IA. Pas d'import retour : les recettes se lisent, point.

## P04.4 — Choix de l'IA · SAFE · low · ✅ DONE (3.19.0)

Feedback Thomas : chips Claude / ChatGPT / Gemini / Copier seulement (préférence mémorisée,
clé `eatwise-llm`), bouton générique « Analyser mes données ». Claude et ChatGPT s'ouvrent
pré-remplis (`?q=`), Gemini s'ouvre avec le rapport copié (pas de pré-remplissage supporté),
« Copier seulement » copie et confirme. Utilisé par l'analyse ET les recettes.

## P04.3 — Docs + gate + déploiement · SAFE · low · ⏳

Section « Prompt Recettes » dans le miroir eatwise-prompt.md, historique de version,
verify.sh (golden buildExport inchangé attendu), prod confirmée.
