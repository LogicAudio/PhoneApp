---
name: eatwise
type: rules
governs:
  - apps/eatwise/
read_when: Avant de toucher quoi que ce soit sous apps/eatwise/ — modèle de données, logique métier, versionnement semver strict.
---

> **Note monorepo (ajoutée à l'intégration dans PhoneApp)** : ce guide a été écrit pour un repo autonome. Ici, EatWise vit dans `apps/eatwise/` :
> - « racine du repo » → **`apps/eatwise/www/`** (c'est là que vivent `index.html`, `manifest.webmanifest`, `sw.js`, `icon.svg`) ;
> - le déploiement GitHub Pages se fait depuis ce dossier (workflow ou config Pages adaptée), pas littéralement depuis la racine du monorepo ;
> - l'enveloppe Capacitor (`android/`) reste disponible pour produire un APK, mais **la phase actuelle est la PWA** ;
> - contrairement aux autres apps du monorepo, EatWise ne référence pas `shared/` : tout est inline dans `index.html` (choix assumé, voir ci-dessous).

# EatWise — Guide du projet

Application personnelle de suivi santé : **digestion (ballonnements)** + **douleurs de spondylarthrite ankylosante**. Elle relie ce qu'on mange, ce qu'on ressent, et fait ressortir les liens. Objectif de cette phase : passer d'un fichier HTML unique à une **PWA installable déployée sur GitHub Pages**.

## Langue & ton
- **Français**, direct et concis. C'est la langue de l'app et des échanges.
- Slogan/identité : « EatWise — Eat wise, feel nice. » Titre : « Écoute ton corps, parle à ton assiette. » Sous-titre : « Observe, comprends, ajuste — et sens-toi mieux. »

## État actuel
- **Un seul fichier `index.html`**, version **3.15.1** (voir `VERSION` dans le code, affichée dans le footer). 3.14.0 = 3.13.0 + câblage PWA (manifest, service worker, icône). 3.15.0 = intensité « Aucune » (sev 0) pour les ballonnements. 3.15.1 = palette rafraîchie (émeraude/menthe/corail) + icône cœur-dans-l'assiette — les fichiers déployés dans `www/` font foi sur l'annexe ci-dessous pour les couleurs.
- **Vanilla JS pur** : aucun framework, aucune dépendance, aucun build, aucun CDN. Tout est inline (HTML + CSS + JS). C'est un choix assumé : ça tourne hors-ligne et sans outillage.
- Rendu maison : un objet `state`, une fonction `render()` qui régénère `#app`, délégation d'événements via attributs `data-act` / `data-field`.
- Stockage : `localStorage` sous la clé `eatwise-v3`, avec **fallback mémoire** (`store.get/set` dans un try/catch) pour ne jamais planter en environnement restreint.

## Objectif immédiat : déploiement PWA sur GitHub Pages
Garder `index.html` tel quel et ajouter, à côté de lui (voir note monorepo) :
1. `manifest.webmanifest`
2. `sw.js` (service worker : cache offline + installabilité)
3. `icon.svg`
Puis : Settings → Pages → Deploy from branch → `main` / `root`.
Le contenu de ces trois fichiers est fourni en **annexe** ci-dessous.
Après ça, `index.html` doit référencer le manifest et enregistrer le service worker (balises `<link rel="manifest">`, `<meta theme-color>`, apple-touch-icon, et un `navigator.serviceWorker.register("sw.js")` en try/catch). Vérifier l'installabilité (Chrome → « Installer l'application »).

## Modèle de données (NE PAS CASSER)
Objet stocké : `{ "entries": [...], "analysis": { "date": "...", "text": "..." } | null }`.

Chaque entrée de `entries` a un `type` :
- `meal`    : `{id, type, date, time, meal (texte libre), tags (string[] aliments), sport? (booléen hérité)}`
- `sport`   : `{id, type, date, time, note}` — effort horodaté
- `symptom` : `{id, type, date, time, sev (0-3, 0 = « Aucune » : observation explicite d'absence), note}` — ballonnements
- `pain`    : `{id, type, date, level (0-10), stiff (bool), note}` — douleur quotidienne (pas d'heure : une par jour)

`analysis.text` est du **markdown léger** : titres préfixés `## `, puces préfixées `- `. Rendu par `renderAnalysis()`.

## Logique métier (à préserver précisément)
- **Ballonnements** — fenêtre rapide. Un *déclencheur* (un `meal`, ou un `sport`, ou un `meal` avec `sport:true` hérité) est « suspect » si un `symptom` de `sev >= 2` survient dans les **4h** (`WINDOW_MS`). On affiche taux et délai médian. Le sport compte comme déclencheur au même titre qu'un aliment (nom unifié « Sport »).
- **tags** générés depuis le texte du repas : split sur virgules/points-virgules/sauts de ligne, normalisation de casse via `normFood()` (« BŒUF »/« bœuf » → « Bœuf »). Voir `tagsFromMeal()`.
- **Douleurs (spondylarthrite)** — réaction **LENTE**. On corrèle la douleur d'un jour J avec les aliments de la **VEILLE (J-1)** et de l'**AVANT-VEILLE (J-2)**, **jamais** le jour même (au réveil, rien n'a encore été mangé de la journée). Minimum 3 jours par aliment pour afficher un écart. Voir `computePain()`.

## Boucle d'analyse (le cœur du produit)
1. L'utilisateur clique **Exporter** → `buildExport()` génère un prompt : posture experte + structure + « ce que je cherche » + « ce que tu dois me renvoyer » (2 parties) + analyse précédente + données JSON.
2. Il colle ce prompt dans **Claude Opus** (idéalement recherche web activée).
3. Claude renvoie : **PARTIE 1** une explication en français (ballonnements / douleurs / suggestions), **PARTIE 2** un petit JSON `{"analysis":{"date","text"}}` — **sans** les entrées.
4. L'utilisateur colle ce JSON dans **Importer** → `applyImport()` met à jour l'analyse et **conserve les données**.

`applyImport()` accepte trois formes : tableau brut (entries), `{entries, analysis?}`, ou `{analysis}` seul. Ne pas régresser sur ce comportement.

## Conventions de versionnement (semver strict)
La version vit dans `var VERSION` (footer). À chaque changement, annoncer et incrémenter :
- **PATCH** (x.x.+1) : cosmétique, texte, correction sans changement de comportement.
- **MINOR** (x.+1.0) : fonctionnalité ou changement de comportement **rétrocompatible** (les anciens exports/imports restent valides).
- **MAJOR** (+1.0.0) : **format de données incompatible**. Dans ce cas seulement, changer aussi la clé de stockage (`eatwise-v3` → `eatwise-v4`) et prévoir une migration, sinon l'utilisateur perd son historique.

## Contraintes & garde-fous
- **Les données sont précieuses, l'app est jetable.** Ne jamais casser la compatibilité de `{entries, analysis}`. Toute évolution doit lire les anciens fichiers.
- Nom de fichier HTML **stable** (`index.html`) et sauvegarde `.json` à **nom fixe** (`eatwise/data/eatwise.json`) pour écraser au lieu d'accumuler.
- Nom de l'app **figé** : « EatWise » (`APP_NAME`).
- **Pas un avis médical.** Garder les disclaimers. Les suggestions sont des **expériences à tester** (« essaie / limite / décale »), jamais des prescriptions. Le lien alimentation-spondylarthrite est incertain scientifiquement → renvoyer vers rhumatologue/diététicien.
- Le prompt interdit d'**inventer des références** (PubMed) si la recherche web n'est pas disponible. Conserver ce garde-fou.
- Après chaque déploiement modifiant le code : **incrémenter le nom du cache** dans `sw.js` (`eatwise-v1` → `eatwise-v2`…), sinon les appareils servent l'ancienne version.

## Pistes futures (non prioritaires)
- Historique d'analyses (plusieurs entrées datées) plutôt qu'une seule.
- Croiser la raideur matinale (`stiff`) avec l'alimentation, en plus du niveau de douleur.
- Petit graphe combiné déclencheurs/symptômes.

---

## Annexe — fichiers PWA à créer

### `manifest.webmanifest`
```json
{
  "name": "EatWise",
  "short_name": "EatWise",
  "description": "Suivi digestion et douleurs, avec analyse des liens.",
  "start_url": "./",
  "scope": "./",
  "display": "standalone",
  "orientation": "portrait",
  "background_color": "#F1ECE0",
  "theme_color": "#1F5C54",
  "icons": [
    { "src": "icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any maskable" }
  ]
}
```

### `sw.js`
```javascript
const CACHE = "eatwise-v1";
const ASSETS = ["./", "./index.html", "./manifest.webmanifest", "./icon.svg"];
self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET") return;
  e.respondWith(
    caches.match(e.request).then((cached) => cached || fetch(e.request).then((res) => {
      const copy = res.clone();
      caches.open(CACHE).then((c) => c.put(e.request, copy)).catch(() => {});
      return res;
    }).catch(() => cached))
  );
});
```

### `icon.svg`
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect width="512" height="512" fill="#1F5C54"/>
  <circle cx="256" cy="256" r="150" fill="none" stroke="#F1ECE0" stroke-width="18"/>
  <path d="M272 148 L206 272 L248 272 L238 364 L314 238 L268 238 Z" fill="#C98A34"/>
</svg>
```

### Balises à ajouter dans `<head>` de `index.html`
```html
<link rel="manifest" href="manifest.webmanifest" />
<link rel="apple-touch-icon" href="icon.svg" />
```
Et, avant `</body>` :
```html
<script>
if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker.register("sw.js").catch(function () {});
  });
}
</script>
```
