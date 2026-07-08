---
status: done
---

# Plan 12 — Recettes réalistes, ancrées culture, petit-déj express

> **Origin (2026-07-08) :** Thomas — « tes recettes sont pas terribles. Le matin je veux une
> recette très facile en 2 minutes (genre ouvrir un paquet de corn flakes). Pour les autres,
> les bons ingrédients c'est bien mais il faut quelque chose de mangeable. Et mettre d'où on
> vient : ne me sors pas du porridge et des trucs totalement anglais si je viens de Belgique —
> rester un peu dans la culture. »

## Context

PATCH-ish MINOR 3.30.0 (touche uniquement le prompt recettes + personnalisation). Le prompt
recettes n'est **pas** couvert par le golden (seul `buildExport` l'est) → aucun recalage.

## P12.1 — Champ « culture culinaire » paramétrable · SAFE · low · ✅ DONE

Ajout `region` aux labels (champ additif, défaut « Belgique — cuisine belge et française du
quotidien »). Carte Personnalisation : nouveau champ libre. Injecté dans le prompt recettes.

## P12.2 — Prompt recettes v2 · SAFE · low · ✅ DONE

- **Petit-déjeuner** : « prêt en 2 minutes, sans cuisson ou presque, ultra simple (verser des
  céréales, tartiner, un yaourt + fruit) ». Pas de plat élaboré le matin.
- **Midi / soir** : de VRAIS plats appétissants que les gens mangent réellement, pas une liste
  d'aliments sains juxtaposés ; ingrédients trouvables au supermarché du coin.
- **Ancrage culturel** : rester dans la cuisine {{région}} ; éviter les plats exotiques ou
  étrangers aux habitudes (ex. pas de porridge à l'anglaise pour un Belge).
- Garde les contraintes santé existantes (aliments tolérés / suspects / analyse). Miroir
  `eatwise-prompt.md` synchronisé.

## P12.3 — Gate + déploiement 3.30.0 · SAFE · low · ✅ DONE (en prod)
