---
status: in-progress
priority: now
---

# Plan 10 — Statistiques d'associations d'aliments → prompt d'analyse

> **Origin (2026-07-03) :** Thomas — « comptabiliser le nombre de fois que l'aliment a causé un
> problème est intéressant parce qu'un problème peut être causé par un autre aliment ou une
> association. ça serait sûrement bien de faire quelques statistiques et de les donner au
> prompt d'analyse en même temps que les données ? comme ça on construit notre propre analyseur ».

## Context

MINOR 3.28.0 (embarque aussi la normalisation 0-10 du ballonnement sur les graphes, 3.27.1
non déployée). Le prompt injecte déjà comptes/taux/délais par aliment (RÉSUMÉ, depuis 3.16.0) ;
on ajoute les **co-occurrences** : paires d'aliments présents ensemble dans la fenêtre de 4 h
avant un épisode (≥ 2 fois), top 6. `buildExport()` change → golden recalé (demande explicite).

## P10.1 — `computeBloatPairs()` + affichage in-app · SAFE · medium · ✅ DONE

Paires triées par fréquence, affichées sous le Top 5 (« Oignon + Bière — ensemble avant
3 épisodes ») ; rien d'affiché sous 2 occurrences.

## P10.2 — Injection dans le prompt + MÉTHODE · SAFE · low · ✅ DONE

Ligne « Associations récurrentes avant épisodes » dans le RÉSUMÉ + consigne MÉTHODE :
utiliser les associations et les repas complets pour départager les co-suspects. Miroir
eatwise-prompt.md synchronisé.

## P10.3 — Gate (golden recalé) + déploiement · SAFE · low · ⏳ gate en cours
