---
status: in-progress
priority: now
---

# Plan 09 — Libellés paramétrables (autres maladies : rougeurs, eczéma…)

> **Origin (2026-07-03) :** Thomas — « il faut aussi que dans l'onglet donnee on puisse
> remplacer douleur et ballonnement par d'autre champs (libre) pour d'autre maladie, rougeurs,
> ecczema, en gros les champs doivent etre parametrable et facile a changer est ce possible ? ».

## Context

MINOR 3.23.0. Décision de conception : la **mécanique ne change pas** (un symptôme « rapide »
horodaté avec intensité 0-3 corrélé aux déclencheurs sur 4 h ; un suivi quotidien 0-10 avec
case du matin corrélé J-1/J-2) — toute l'analyse repose dessus et les types stockés restent
`symptom`/`pain`. Ce qui devient paramétrable : les **libellés** (symptôme rapide, suivi
quotidien, case du matin) et la **situation santé** injectée dans les prompts IA. Champ
**additif** `labels` dans l'objet stocké (backup/restauration inclus, anciens fichiers
valides). Prompts paramétriques → golden `buildExport` recalé une fois (les changements de
libellés par l'utilisateur n'affectent plus le golden : la fixture sans `labels` = défauts).

## P09.1 — Champ additif `labels` + carte Personnalisation · SAFE · medium · ✅ DONE

`labels` = `{fast, daily, flag, condition}` (défauts : Ballonnement / Douleur / Raideur
matinale / digestion et spondylarthrite). Carte dans Données avec 4 champs libres ; champ
vidé = retour au défaut ; persistance immédiate, re-rendu au blur.

## P09.2 — Libellés propagés partout · SAFE · high · ✅ DONE (+ PREMIÈRE TÂCHE de détection de spécialité dans le prompt, demande Thomas)

Tuiles, formulaires, Journal, Analyse (titres de sections, graphe, carte du matin), badge,
rapport médecin (la note « raideur ≥ 30 minutes = inflammatoire » ne s'affiche que si la case
du matin garde son sens par défaut), prompts d'analyse et de recettes (situation santé).

## P09.4 — Bouton « Buy me a coffee » · SAFE · low · ✅ DONE (3.23.1)

Page créée par Thomas (buymeacoffee.com/logicaudio) : lien ☕ dans le footer + carte
« Soutenir EatWise » dans Données. App gratuite, dons volontaires.

## P09.3 — Docs + gate (golden recalé) + déploiement · SAFE · low · ⏳ gate OK, déploiement bloqué par un incident intermittent GitHub Pages (deploy-pages), relances en cours
