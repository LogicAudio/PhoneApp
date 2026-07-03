#!/usr/bin/env node
// Goldens du cœur fragile EatWise — déterministe, ZÉRO token LLM, hors-ligne.
//
// Extrait le <script> applicatif d'apps/eatwise/www/index.html, l'évalue dans une
// sandbox node:vm (stubs DOM minimaux, pas de localStorage → fallback mémoire de
// l'app), puis fige les sorties des fonctions métier contre scripts/goldens/eatwise.json :
//   - normFood / tagsFromMeal (normalisation + dédup des aliments)
//   - computeBloat            (fenêtre 4h, sev>=2, sport déclencheur)
//   - computePain             (corrélation J-1/J-2, seuil 3 jours) — champ `days` exclu
//                             (il dépend du jour courant, non déterministe)
//   - applyImport             (3 formes acceptées + erreurs, messages alert inclus)
//   - renderAnalysis          (markdown léger → HTML, échappement)
//   - buildExport             (prompt d'analyse complet, todayISO figé)
//
// Usage :
//   node scripts/eatwise_golden.mjs             # --check implicite : diff vs baseline, exit≠0 si écart
//   node scripts/eatwise_golden.mjs --update    # recale la baseline — DÉLIBÉRÉ, accord humain requis
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import vm from "node:vm";

const HTML_PATH = new URL("../apps/eatwise/www/index.html", import.meta.url);
const FIXTURE_PATH = new URL("./goldens/eatwise_fixture.json", import.meta.url);
const BASELINE_PATH = new URL("./goldens/eatwise.json", import.meta.url);
const FROZEN_TODAY = "2026-01-15";

function buildSandbox() {
  const appEl = { innerHTML: "", addEventListener() {} };
  const alerts = [];
  const ctx = {
    document: {
      getElementById: () => appEl,
      createElement: () => ({ style: {} }),
      body: { appendChild() {}, removeChild() {} },
    },
    alert: (msg) => alerts.push(String(msg)),
    navigator: {},
    window: { addEventListener() {} },
    console,
  };
  vm.createContext(ctx);
  return { ctx, alerts };
}

function computeOutputs() {
  const html = readFileSync(HTML_PATH, "utf8");
  const m = html.match(/<script>([\s\S]*?)<\/script>/);
  if (!m) throw new Error("aucun <script> trouvé dans index.html");
  const fixture = JSON.parse(readFileSync(FIXTURE_PATH, "utf8"));

  const { ctx, alerts } = buildSandbox();
  vm.runInContext(m[1], ctx);
  ctx.todayISO = () => FROZEN_TODAY; // fige la date pour applyImport (défaut) et buildExport

  const out = {};
  out.normFood = fixture.normCases.map((s) => ({ input: s, out: ctx.normFood(s) }));
  out.tags = fixture.tagCases.map((t) => ({ input: t, tags: ctx.tagsFromMeal(t) }));
  out.bloat = ctx.computeBloat(fixture.entries);
  const pain = ctx.computePain(fixture.entries);
  delete pain.days; // fenêtre glissante sur le jour courant — non déterministe
  out.pain = pain;
  out.imports = fixture.importCases.map((c) => {
    ctx.state.entries = [];
    ctx.state.analysis = null;
    alerts.length = 0;
    ctx.applyImport(JSON.parse(JSON.stringify(c.payload)));
    return { name: c.name, entries: ctx.state.entries, analysis: ctx.state.analysis, alerts: alerts.slice() };
  });
  out.renderAnalysis = fixture.analysisTexts.map((t) => ({ input: t, html: ctx.renderAnalysis(t) }));
  ctx.state.entries = fixture.entries;
  ctx.state.analysis = fixture.analysis;
  out.exportPrompt = ctx.buildExport();
  return out;
}

function firstDiff(a, b) {
  const la = a.split("\n"), lb = b.split("\n");
  for (let i = 0; i < Math.max(la.length, lb.length); i++) {
    if (la[i] !== lb[i]) {
      return [
        `  première divergence ligne ${i + 1} :`,
        `    baseline : ${la[i] === undefined ? "<absente>" : la[i]}`,
        `    actuel   : ${lb[i] === undefined ? "<absente>" : lb[i]}`,
      ].join("\n");
    }
  }
  return "";
}

const update = process.argv.includes("--update");
const actual = JSON.stringify(computeOutputs(), null, 2) + "\n";

if (update) {
  const old = existsSync(BASELINE_PATH) ? readFileSync(BASELINE_PATH, "utf8") : null;
  writeFileSync(BASELINE_PATH, actual);
  if (old === null) console.log("🟡 baseline créée : scripts/goldens/eatwise.json");
  else if (old === actual) console.log("✅ baseline inchangée — rien à recaler.");
  else {
    console.log("🟡 baseline RECALÉE — mise à jour délibérée, à justifier (CLAUDE.md : accord humain).");
    console.log(firstDiff(old, actual));
  }
  process.exit(0);
}

if (!existsSync(BASELINE_PATH)) {
  console.error("❌ goldens : baseline absente (scripts/goldens/eatwise.json). Créer : node scripts/eatwise_golden.mjs --update");
  process.exit(1);
}
const baseline = readFileSync(BASELINE_PATH, "utf8");
if (baseline === actual) {
  console.log("✅ goldens EatWise : la logique métier d'index.html correspond à la baseline.");
  process.exit(0);
}
console.error("❌ goldens EatWise : la logique métier a DIVERGÉ de la baseline.");
console.error(firstDiff(baseline, actual));
console.error("  → corrige la régression, ou si le changement est voulu et validé par Thomas :");
console.error("    node scripts/eatwise_golden.mjs --update");
process.exit(1);
