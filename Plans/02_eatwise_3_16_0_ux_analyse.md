---
status: in-progress
priority: now
---

# Plan 02 — EatWise 3.16.0 : refonte visuelle + boucle d'analyse sans friction

> **Origin (2026-07-03) :** Thomas — « les couleurs sont un peu tristounette pour une app de
> santé, aussi le logo n'est pas du tout en relation avec l'app » (référence visuelle : capture
> Gluci-Chek) ; « improve the app, make it better, simple and intuitive, well explained, I feel
> all the interface with the json is not friendly. refine the prompt analysis for claude health
> care, propose new functionnalities idea of recipes » ; « un button qui ouvre gemini ou claude
> avec la copie du json en argument ? ».

## Context

MINOR 3.16.0 (rétrocompatible : clé `eatwise-v3` et format `{entries, analysis}` intacts,
`applyImport()` inchangé). Le prompt `buildExport()` change → recalage délibéré du golden,
couvert par la demande explicite de Thomas (« refine the prompt analysis »). Gate :
`scripts/verify.sh` avant commit (hook pre-commit actif sur le cœur fragile).

## P02.1 — Palette « Gluci-Chek » · SAFE · low · ✅ DONE

Fond quasi blanc `#F6F7F8`, cartes blanches ombrées, une couleur par fonction : Mangé sarcelle
`#2EB39A` (= brand/header/tabs), Ballonné orange `#F19A4D`, Douleur corail `#E56A73`, Sport
violet `#8C7AE6` (nouvelle var `--sport`). SEV recolorés (Aucune vert doux → Fort corail).

## P02.2 — Onglet Données sans jargon · SAFE · medium · ✅ DONE

Deux étapes au lieu du vocabulaire export/import/JSON : ① bouton « Envoyer mes données à
Claude » (copie le prompt + ouvre `claude.ai/new`, pré-rempli via `?q=` si l'URL reste sous
~6 000 caractères encodés, sinon repli collage — Gemini : pas de pré-remplissage fiable,
non retenu) ; ② zone « Colle la réponse de Claude » avec extraction tolérante `extractJSON()`
(accepte la réponse complète, retrouve le bloc `{"analysis": ...}` par balance d'accolades).
`applyImport()` et ses 3 formes restent inchangés (golden).

## P02.3 — Prompt santé v2 · SAFE · medium · ✅ DONE (miroir réviewable : Knowledge/eatwise-prompt.md ; golden recalé délibérément)

Résumé chiffré calculé par l'app injecté dans le prompt (suspects, délais, deltas douleur),
section MÉTHODE (corrélation ≠ causalité, niveaux de confiance, familles FODMAP, seuil
3 observations, signaux d'alerte → médecin), garde-fou anti-références-inventées conservé,
PARTIE 2 au format JSON identique.

## P02.4 — Recettes dans la boucle d'analyse · SAFE · low · ✅ DONE

« IDÉES RECETTES » demandées en PARTIE 1 (2-3 repas sur aliments bien tolérés, alternatives)
et titre `## Recettes` autorisé dans `analysis.text` — zéro changement de modèle de données.

## P02.5 — Icône anti-cache + PNG · SAFE · low · ✅ DONE

Android fige l'icône du WebAPK tant que l'URL ne change pas → renommage `icon.svg` →
`icon-2.svg` recoloré (sarcelle/corail) + `icon-192.png`/`icon-512.png` (rasterisés via
qlmanage) référencés en premier dans le manifest. `apple-touch-icon` → PNG.

## P02.6 — Version + docs · SAFE · low · ✅ DONE

`VERSION` 3.16.0, cache sw `eatwise-v4`, `ASSETS` mis à jour, `Knowledge/eatwise.md`
(historique versions, description du nouveau flux Données, note icônes).

## P02.7 — Gate + déploiement · SAFE · low · ⏳ gate OK, déploiement en cours

`scripts/verify.sh` (recalage golden `buildExport` délibéré), tests de rendu Node, commit,
push, déploiement Pages confirmé en production (footer 3.16.0).

## Idées notées, hors périmètre 3.16.0 (proposer à Thomas)

- Répéter un repas en un tap depuis le Journal (« encore ce repas »).
- Rappels quotidiens (notification) — nécessite l'enveloppe APK/Capacitor.
- Historique d'analyses datées (piste déjà au guide).
- Croiser raideur matinale × alimentation (piste déjà au guide).
- `navigator.storage.persist()` pour blinder le localStorage.
