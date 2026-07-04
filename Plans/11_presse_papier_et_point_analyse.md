---
status: done
---

# Plan 11 — Import presse-papier (si ça marche) + point de rappel d'analyse

> **Origin (2026-07-04) :** Thomas a trié le backlog : I8 « oui si ça marche », I9 « oui mais
> light, un petit point qui s'allume ». I2, I4, I7, I11 et durée de raideur : non.

## Context

MINOR 3.29.0. Deux contraintes de conception posées par Thomas :
- **I8** : la lecture du presse-papier (`navigator.clipboard.readText`) dépend d'une permission
  navigateur — l'implémentation doit **échouer en silence** si refusée/indisponible, ne jamais
  importer sans confirmation (bannière « Analyse détectée — Enregistrer ? »), et ne jamais
  re-proposer le même contenu. Try/catch autour de `document.addEventListener` pour ne pas
  casser la sandbox du golden.
- **I9** : pas de carte, pas de message — un **point sarcelle** sur l'onglet Analyse quand
  l'analyse est « périmée » : aucune analyse et ≥ 5 entrées, ou ≥ 10 entrées plus récentes
  qu'elle, ou analyse vieille de ≥ 14 jours.

## P11.1 — Bannière presse-papier · SAFE · medium · ✅ DONE

Au retour dans l'app (visibilitychange/focus) et à l'ouverture de l'onglet Analyse : tentative
de lecture silencieuse ; si un bloc `{"analysis"...}` différent de l'analyse courante est
trouvé → bannière sous les onglets avec [Enregistrer] / [Ignorer]. Import via `applyImport`
existant (golden intact).

## P11.2 — Point « analyse à rafraîchir » · SAFE · low · ✅ DONE

`analysisStale()` + point sur l'onglet Analyse (distinct du point corail « douleur non notée »
sur Ajouter).

## P11.3 — Gate + déploiement · SAFE · low · ✅ DONE (3.29.0 en prod)
