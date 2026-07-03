---
status: done
---

# Plan 08 — Retirer les recettes de la boucle d'analyse

> **Origin (2026-07-03) :** Thomas — « c'est plutot le json d'analyse ou il y a une recette qui
> doit etre couper i.e. ne pas retourner de recette puisqu'il y a deja un onglet recette propre
> a ca » (après annulation d'une première interprétation : pas de retour JSON des recettes
> dans l'app).

## Context

MINOR 3.22.0. Séparation nette des deux circuits : l'analyse (onglet Analyse, avec retour
JSON `{"analysis"...}`) ne demande plus d'idées recettes ; les recettes vivent uniquement
dans l'onglet Recettes (lecture directe dans l'IA, pas de retour). `buildExport()` change →
recalage délibéré du golden, couvert par la demande explicite ci-dessus.

## P08.1 — Prompt d'analyse sans recettes · SAFE · low · ✅ DONE

Supprimer de `buildExport()` : le point « 3) idées de repas », la sous-partie « IDÉES
RECETTES » de PARTIE 1, et `'## Recettes'` de la liste de titres de PARTIE 2. Miroir
`eatwise-prompt.md` synchronisé (note de conception mise à jour). Texte UI « avec des idées
recettes » retiré de la carte d'analyse.

## P08.2 — Gate (golden recalé) + déploiement 3.22.0 · SAFE · low · ✅ DONE (confirmée en prod)
