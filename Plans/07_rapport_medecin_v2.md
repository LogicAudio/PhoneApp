---
status: done
---

# Plan 07 — Rapport médecin v2 (état de l'art du reporting alimentation/rhumatologie)

> **Origin (2026-07-03) :** Thomas — « le rapport pour le medecin peut etre mieux fait, pas
> d'abreviation, et une liste de ce qui a ete mange et l'etat apres, nombre d'heure douleur.
> le rapport doit etre utile, peut etre visuel, renseigne toi sur le state of the art » ;
> « le rapport est trop petit dans l'app, bouton imprimer ou exporter en pdf ? ».

## Context — recherche (2026-07-03)

Deux référentiels combinés :
- **Journal aliments-symptômes** (diététique/gastro-entérologie — Stanford Health Care, World
  Gastroenterology Organisation, IFFGD) : chaque prise alimentaire avec heure et description,
  symptôme noté en regard avec sévérité et délai/durée, facteurs de vie (activité physique),
  période recommandée de 1 à 2 semaines, rempli au fil de l'eau.
- **BASDAI** (rhumatologie — Bath Ankylosing Spondylitis Disease Activity Index) : échelle
  numérique 0-10, la durée de raideur matinale compte autant que son intensité (raideur
  ≥ 30 minutes = marqueur de douleur inflammatoire ; BASDAI ≥ 4 = maladie active).
  ⚠️ L'app ne trace pas la **durée** de raideur (booléen seulement) — limitation signalée
  dans le rapport ; champ « durée » proposé au backlog (décision Thomas, modèle de données).

## P07.1 — Rapport v2 · SAFE · medium · ✅ DONE (+ axe Y et rangée de marqueurs séparée sur le graphe in-app, feedback Thomas « deux échelles différentes »)

1. **Lisible sur téléphone** : balise viewport (cause du texte minuscule), police 15 px,
   bouton « Imprimer / Enregistrer en PDF » (`window.print()`, masqué à l'impression).
2. **Zéro abréviation** : « la veille ou l'avant-veille », intensités en toutes lettres,
   délais en « X heures YY ».
3. **Synthèse clinique** : période et complétude du journal (jours renseignés / jours de la
   période), douleur moyenne/maximale (échelle numérique 0-10), jours à douleur ≥ 4,
   raideur matinale (x matins / y), épisodes de ballonnements par intensité, délai médian
   déclencheur → ballonnement en heures.
4. **Courbe visuelle** : barres de douleur des 28 derniers jours + marqueurs ballonnements,
   couleurs forcées à l'impression (print-color-adjust).
5. **Journal aliments-symptômes des 14 derniers jours** (format diététicien) : jour par jour,
   chaque repas (heure + aliments), chaque ballonnement (intensité en toutes lettres + délai
   après le déclencheur précédent), sport, douleur du jour avec raideur.
6. **Corrélations** en toutes lettres + **Méthode & limites** (fenêtre de 4 heures,
   corrélation veille/avant-veille, seuil de 3 jours, auto-observation, pas un avis médical).

## P07.2 — Gate + déploiement 3.21.0 · SAFE · low · ✅ DONE (confirmée en prod)
