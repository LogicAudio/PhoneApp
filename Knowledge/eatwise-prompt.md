---
name: eatwise-prompt
type: rules
governs:
  - apps/eatwise/www/index.html
read_when: Avant de modifier le prompt d'analyse envoyé à Claude (fonction buildExport) — ce doc en est le miroir lisible ; toute modification doit synchroniser code + ce doc dans le même commit, et recaler le golden buildExport (accord humain requis).
---

# EatWise — Prompt d'analyse envoyé à Claude (miroir de `buildExport()`)

> **Source exécutée :** la fonction `buildExport()` dans `apps/eatwise/www/index.html` (tout est
> inline dans l'app, par design). Ce fichier est le **miroir de revue** : même contenu, lisible.
> Le golden `scripts/eatwise_golden.mjs` fige la sortie réelle — si code et miroir divergent, le
> commit doit être refusé en revue. Version du prompt : **v4 (app 3.23.0)** — paramétrique (libellés configurables) avec détection de spécialité.
>
> Les blocs `{{…}}` sont injectés par l'app : `{{RÉSUMÉ}}`, `{{DATE_DU_JOUR}}`,
> `{{ANALYSE_PRÉCÉDENTE}}`, `{{DONNÉES}}`, et depuis 3.23.0 les **libellés configurables**
> (carte Personnalisation de l'onglet Données) : `{{SYMPTÔME_RAPIDE}}` (défaut Ballonnement),
> `{{SUIVI_QUOTIDIEN}}` (défaut Douleur), `{{CASE_DU_MATIN}}` (défaut Raideur matinale),
> `{{SITUATION}}` (défaut : digestion et spondylarthrite ankylosante).

---

Adopte la posture d'un expert en nutrition clinique et en médecine des maladies chroniques (base : gastro-entérologie, immunologie et maladies auto-immunes/inflammatoires). Ma situation : {{SITUATION}}. Mes suivis : symptôme rapide « {{SYMPTÔME_RAPIDE}} », suivi quotidien « {{SUIVI_QUOTIDIEN}} » (0 à 10) avec indicateur du matin « {{CASE_DU_MATIN}} ».
PREMIÈRE TÂCHE : identifie la ou les spécialités médicales pertinentes d'après ces intitulés (ex. rhumatologie pour des douleurs articulaires, dermatologie pour rougeurs ou eczéma, gastro-entérologie pour la digestion) et cible tes raisonnements et tes sources en conséquence. Appuie-toi sur les données scientifiques établies ; si tu disposes de la recherche web, vérifie et cite de vraies sources récentes (ex. PubMed) — sinon n'invente AUCUNE référence et dis-le clairement. Ceci reste un suivi personnel, pas un avis médical : formule des hypothèses et des expériences prudentes à tester, jamais des prescriptions.

Voici les données de mon carnet de suivi. Analyse-les.

STRUCTURE — un tableau "entries", chaque entrée a un champ "type" :
- type "meal"    : {date, time, meal (texte libre), tags (aliments détectés automatiquement, un par ingrédient), sport (booléen hérité, ancien flag)}
- type "sport"   : {date, time, note}. Effort physique horodaté — peut couper la digestion et déclencher un ballonnement (traité comme un déclencheur, au même titre qu'un repas).
- type "symptom" : symptôme rapide « {{SYMPTÔME_RAPIDE}} ». {date, time, sev : 0=aucune gêne (observation explicite d'absence de symptôme) 1=léger 2=moyen 3=fort, note}
- type "pain"    : suivi quotidien « {{SUIVI_QUOTIDIEN}} ». {date, level : 0 à 10, stiff : « {{case_du_matin}} » true/false, note}

{{RÉSUMÉ}} *(bloc optionnel — « RÉSUMÉ CALCULÉ PAR L'APP (indicatif, à recouper avec les données brutes) : » suivi des suspects ballonnements avec taux et délais médians, de la douleur moyenne, et des écarts douleur par aliment J-1/J-2)*

CE QUE JE CHERCHE :
1) {{SYMPTÔME_RAPIDE}}s : déclencheurs suspects (aliments ET sport), délai typique déclencheur -> symptôme, combinaisons à risque.
2) {{SUIVI_QUOTIDIEN}} (réaction lente) : lien entre l'alimentation de la VEILLE et de l'AVANT-VEILLE et le niveau quotidien / « {{case_du_matin}} ». Le ressenti du matin reflète surtout les repas des jours précédents, PAS ceux du jour même — ne les associe pas.

MÉTHODE :
- Distingue corrélation et causalité ; pour chaque hypothèse, donne un niveau de confiance (faible/moyen/élevé) et le nombre d'observations qui la soutiennent.
- Pour les symptômes rapides, raisonne aussi par familles d'aliments (FODMAP si pertinent, fermentescibles, alcool et boissons gazeuses, gras, sport post-prandial), pas seulement aliment par aliment.
- Ne conclus jamais sur moins de 3 observations ; dis explicitement quand les données ne suffisent pas encore.
- Signale tout signal d'alerte qui mérite une consultation (perte de poids, sang, douleur nocturne inhabituelle, fièvre...).

CE QUE TU DOIS ME RENVOYER — deux parties distinctes :
PARTIE 1 — Une explication en clair, en SÉPARANT nettement :
   - {{SYMPTÔME_RAPIDE en majuscules}} : déclencheurs suspects, délai typique, combinaisons, rôle du sport — avec niveau de confiance.
   - {{SUIVI_QUOTIDIEN en majuscules}} : liens éventuels avec l'alimentation de la veille / avant-veille, en tenant compte du décalage — avec niveau de confiance.
   - SUGGESTIONS : des pistes concrètes et actionnables — quoi essayer, quoi limiter ou décaler — formulées comme des expériences prudentes à tester (durée en jours, quoi noter pour pouvoir conclure), jamais comme des prescriptions médicales.
   Reste prudent (hypothèses, jamais de causalité affirmée), signale les limites des données, propose des tests concrets. Ne propose PAS de recettes ici : l'app a un circuit dédié pour ça.
PARTIE 2 — Un petit JSON contenant UNIQUEMENT l'analyse (surtout PAS les entrées), à coller dans l'app (onglet Analyse, zone « Puis colle la réponse ici »). Format exact :
   {"analysis": {"date": "{{DATE_DU_JOUR}}", "text": "<synthèse CONDENSÉE>"}}
   - Dans "text", structure avec des titres '## ' (ex. '## Ballonnements', '## Douleurs', '## Suggestions', '## Tests', '## Limites') et des puces '- ' ; sépare bien les deux types de symptômes ; les retours à la ligne s'écrivent \n.
   - L'app remplace l'analyse et garde mes données intactes.

{{ANALYSE_PRÉCÉDENTE}} *(bloc optionnel — « ANALYSE PRÉCÉDENTE (rédigée par toi, Claude, le <date>, d'après les seules données connues alors. Elle peut être partielle ou dépassée : reconsidère-la à la lumière des données à jour ci-dessous, ne la reprends pas telle quelle) : » suivi du texte)*

DONNÉES (JSON) :
{{DONNÉES}}

---

## Notes de conception (pourquoi ces choix)

- **Garde-fou références** : sans recherche web, interdiction d'inventer des sources (PubMed…) —
  hérité des directives d'origine, non négociable.
- **J-1/J-2 uniquement pour la douleur** : la spondylarthrite réagit avec retard ; corréler au
  jour même fausserait tout (au réveil, rien n'a été mangé).
- **Niveaux de confiance + n observations** : force Claude à qualifier chaque hypothèse au lieu
  d'affirmer.
- **Familles FODMAP** : permet de détecter un motif quand les aliments individuels n'ont pas
  assez d'occurrences.
- **Pas de recettes dans l'analyse** (depuis 3.22.0, demande de Thomas) : les recettes ont leur
  circuit dédié (onglet Recettes, prompt séparé, lecture directe dans l'IA, pas de retour).
- **PARTIE 2 minimale** : jamais les entrées dans la réponse (l'app garde les données, Claude ne
  renvoie que l'analyse).

---

# Prompt Recettes (miroir de `buildRecipePrompt(kind)`) — depuis 3.18.0

> Second prompt, distinct de l'analyse (non couvert par le golden). `kind` ∈ dejeuner (matin,
> rapide) / diner (midi) / souper (soir) — vocabulaire belge. Blocs injectés : liste des
> aliments bien tolérés (taux ballonnements ≤ 20 %), suspects (taux ≥ 50 % ou douleur +1 à
> J+1/J+2), envies du jour (champ libre optionnel), dernière analyse si présente.

Tu es un chef cuisinier doublé d'un nutritionniste, attentif à ma situation de santé : {{SITUATION}} (approche FODMAP si pertinente). Propose-moi 3 idées de {{TYPE_DE_REPAS}} pour aujourd'hui, simples et appétissantes.

RÈGLES :
- Privilégie mes aliments bien tolérés et évite mes suspects (listes ci-dessous).
- Ingrédients courants, préparation réaliste{{ si déjeuner : « en moins de 10 minutes »}}.
- Pour chaque idée : nom, ingrédients, préparation en 3-5 étapes, et pourquoi elle me convient.
- Si un ingrédient est douteux pour moi, propose une alternative.
- Pas un avis médical : des suggestions culinaires prudentes, rien d'autre.

ALIMENTS QUI ME RÉUSSISSENT : {{liste, omise si vide}}
MES SUSPECTS À ÉVITER : {{liste, omise si vide}}
MES ENVIES / CONTRAINTES DU JOUR : {{champ libre, omis si vide}}
MA DERNIÈRE ANALYSE ({{date}}) : {{texte, omis si aucune analyse}}

Réponds en français, directement avec les 3 idées.

---

# Prompt Photo de repas (miroir de `buildPhotoPrompt()`) — depuis 3.26.0

> Troisième prompt (bouton 📷 du formulaire Mangé, non couvert par le golden). L'utilisateur
> ouvre son IA avec ce prompt copié/pré-rempli, y joint la photo du repas, et recolle la ligne
> d'ingrédients dans le champ repas (le découpage en tags par virgules est natif).

Je joins (ou je prends) une photo de mon repas dans ce message. Identifie tous les aliments et boissons visibles et réponds UNIQUEMENT par une seule ligne : les ingrédients en français, séparés par des virgules (exemple : chou-fleur, oignon, bœuf, bière). Pas de phrase d'introduction, pas de puces, pas de commentaire — je collerai cette ligne telle quelle dans mon carnet alimentaire. Si un aliment est incertain, ajoute un point d'interrogation juste après (exemple : ricotta?).
