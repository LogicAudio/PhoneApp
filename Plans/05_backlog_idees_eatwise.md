---
status: proposed
---

# Plan 05 — Backlog d'idées EatWise (à prioriser par Thomas)

> **Origin (2026-07-03) :** Thomas — « je pense qu'il y a plein d'autres idees comme ca que tu
> peux avoir : ecris un plan d'idee pour ameliorer l'app et implemente le ou demande moi les
> idees a implementer ».

## Context

Idées classées par thème, chacune compatible avec le modèle de données (aucun MAJOR).
Celles que Thomas retient deviennent des plans numérotés et implémentés dans l'ordre choisi.

## Saisie & Journal

- **I1 — Édition d'une entrée** : corriger date/heure/texte/intensité au lieu de
  supprimer-recréer. (medium)
- **I2 — Aliments récents en un tap** : chips des aliments les plus fréquents au-dessus du
  champ repas — la saisie quotidienne devient 2 taps. (low)
- **I3 — Badge « douleur du jour non notée »** : pastille sur l'onglet Ajouter tant que la
  douleur quotidienne n'est pas loguée — c'est la donnée la plus précieuse et la plus facile
  à oublier. (low)
- **I4 — Recherche/filtre dans le Journal** : par aliment ou par type d'entrée. (medium)

## Analyse & graphiques

- **I5 — Raideur matinale × alimentation** : le champ `stiff` est collecté mais inexploité —
  taux de raideur selon les aliments de la veille/avant-veille (même méthode J-1/J-2). (medium)
- **I6 — Graphe combiné 14 jours** : douleur (barres) + ballonnements (points) + jours à
  suspects, en un seul coup d'œil. (medium)
- **I7 — Tendance longue** : douleur moyenne par semaine sur 8-12 semaines — voir si ça
  s'améliore. (low)

## Boucle IA

- **I8 — Import encore plus fluide** : au retour dans l'app, si le presse-papier contient une
  analyse, proposer « Enregistrer l'analyse copiée ? » en un tap (lecture clipboard soumise à
  permission navigateur — best effort). (medium)
- **I9 — Rappel d'analyse** : suggérer une mise à jour de l'analyse après N nouvelles entrées
  ou X jours. (low)

## Partage & médecin

- **I10 — Export pour le rhumatologue** : rapport imprimable (page HTML propre à imprimer en
  PDF) : résumé, graphes, liste des suspects — à poser sur le bureau du médecin. (medium)

## Natif (APK Capacitor — toolchain déjà prête)

- **I11 — Rappels quotidiens** : notification locale « note ta douleur du jour » — nécessite
  de basculer sur l'APK installé en parallèle de la PWA. (high)
