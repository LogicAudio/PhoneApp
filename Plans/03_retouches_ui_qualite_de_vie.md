---
status: in-progress
priority: now
---

# Plan 03 — Retouches UI mobile + qualité de vie

> **Origin (2026-07-03) :** Thomas — « les couleurs sont toujours moche […] les bouton sont un
> peut petit, c'est pas l'interface agreable pour un telephone, je t'avais mis un exemple
> d'image » ; « ne mets pas envoyer mes donnee a claude mais […] analyser mes donnees avec
> claude » ; puis « continue a ameliorer l'app ».

## Context

Suite directe du Plan 02 : coller à la référence visuelle (grille de grosses tuiles colorées),
puis dérouler les améliorations de qualité de vie notées hors périmètre du Plan 02. Compat
données intacte partout (clé `eatwise-v3`, formes d'`applyImport`).

## P03.1 — UI mobile façon référence · SAFE · low · ✅ DONE (3.16.1)

Sélecteur d'entrée = grille 2×2 de grosses tuiles colorées (emoji 28px, active pleine couleur,
inactives teintées 11 %), boutons 16px de padding / 17px de police, onglets et champs
agrandis, libellé « Analyser mes données avec Claude », couleurs plus franches
(sarcelle `#3FBAA0`, orange `#F09A4E`, corail `#E2707B`, violet `#8B7BC7`).

## P03.2 — Blindage du stockage · SAFE · low · ✅ DONE

`navigator.storage.persist()` au chargement (best-effort, try/catch) : demande au navigateur
de ne jamais purger le localStorage — les données sont précieuses.

## P03.3 — Mises à jour instantanées · SAFE · medium · ✅ DONE

`sw.js` : network-first pour les navigations (la page), cache-first pour le reste. Fini le
cycle « ouvrir/fermer/rouvrir » et la confusion « je vois encore l'ancienne version » ; le
hors-ligne reste intact (repli cache sans réseau).

## P03.4 — « Encore » sur les repas du Journal · SAFE · low · ✅ DONE

Bouton « ↻ Encore » sur chaque fiche repas : re-logue le même repas à la date/heure
actuelles en un tap (le cas « je remange pareil » est quotidien).

## P03.5 — Historique d'analyses datées · SAFE · medium · ✅ DONE (champ additif ; golden inchangé, aucun recalage nécessaire)

Piste du guide : conserver les analyses précédentes (champ additif `analysisHistory`, plafonné
à 10, dans l'objet stocké — les anciens exports restent lisibles, `applyImport` inchangé dans
ses 3 formes). Onglet Analyse : l'analyse courante + dépliant « analyses précédentes ».
⚠️ Si le golden `applyImport` bouge (état capturé), recalage à faire valider par Thomas.

## P03.7 — Carte d'analyse dans l'onglet Analyse + note multi-IA · SAFE · low · ✅ DONE

Feedback Thomas : l'action d'analyse vit dans l'onglet Analyse (Données ne garde que la
sauvegarde) ; mention explicite que le rapport se colle dans n'importe quelle IA.

## P03.6 — Gate + déploiement 3.17.0 · SAFE · low · ⏳ gate OK, déploiement en cours

verify.sh, tests Node, push, prod confirmée.

## Idées restantes (backlog, non planifiées)

- Édition d'une entrée existante (aujourd'hui : suppression seulement).
- Corrélation raideur matinale × alimentation affichée dans l'app.
- Rappels quotidiens (nécessite l'APK Capacitor).
- Graphe combiné déclencheurs/symptômes.
