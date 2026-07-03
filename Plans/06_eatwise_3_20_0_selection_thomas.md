---
status: in-progress
priority: now
---

# Plan 06 — EatWise 3.20.0 : la sélection de Thomas (5 fonctionnalités du backlog)

> **Origin (2026-07-03) :** Thomas a priorisé le backlog du Plan 05 : badge « douleur non
> notée », édition d'une entrée, raideur × alimentation, graphe combiné 14 jours, rapport
> imprimable pour le rhumatologue.

## Context

MINOR 3.20.0, compat données intacte. `buildExport()` non touché (golden stable). Les
nouvelles fonctions de calcul (`computeStiff`) ne sont pas encore couvertes par le golden —
extension de la baseline à proposer plus tard (accord humain requis pour tout recalage).

## P06.1 — Badge « douleur du jour non notée » (I3) · SAFE · low · ✅ DONE

Point corail sur l'onglet Ajouter et sur la tuile Douleur tant qu'aucune entrée `pain` du
jour n'existe.

## P06.2 — Édition d'une entrée (I1) · SAFE · medium · ✅ DONE

Bouton « Modifier » sur chaque fiche du Journal → recharge l'entrée dans le formulaire
Ajouter (mode édition, bouton « Mettre à jour », lien « Annuler ») ; la sauvegarde remplace
l'entrée en place (même id). Pour la douleur, l'invariant « une par jour » est préservé.

## P06.3 — Raideur matinale × alimentation (I5) · SAFE · medium · ✅ DONE

`computeStiff()` : même méthode J-1/J-2 que la douleur — % de matins raides quand l'aliment
a été mangé la veille/avant-veille vs sans (min. 3 jours). Carte « Raideur matinale » dans
l'onglet Analyse, sous les douleurs.

## P06.4 — Graphe combiné 14 jours (I6) · SAFE · medium · ✅ DONE

Le graphe douleur gagne deux marqueurs par jour : ● orange = ballonnement (sev ≥ 2),
◆ sarcelle = repas contenant un suspect (taux ≥ 50 %). Légende sous le graphe.

## P06.5 — Rapport rhumatologue (I10) · SAFE · medium · ✅ DONE

Carte « Pour ton médecin » dans Données : bouton qui ouvre une page imprimable autonome
(période couverte, douleur moyenne/max, % raideur, suspects ballonnements, écarts douleur
J-1/J-2, dernière analyse, disclaimer « suivi personnel, pas un avis médical ») — à imprimer
en PDF depuis le navigateur.

## P06.6 — Gate + déploiement · SAFE · low · ⏳ gate en cours
