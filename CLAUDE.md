# CLAUDE.md — PhoneApp Context Map

> **What this is.** Monorepo of Android apps built with Capacitor: each app is plain web code
> (HTML/CSS/JS in `apps/<name>/www/`) wrapped into a native Android app — Android-first, iOS-ready.
> Pipeline in one line: `apps/<name>/www/` → Capacitor wrap → APK (and for EatWise: `www/` →
> GitHub Pages → installable PWA). Current apps: **eatwise** — EatWise, personal health tracking
> (digestion + spondylarthritis pain), in French, PWA-first. Detailed behaviour lives in
> `Knowledge/` (one doc per component, each with `governs:` frontmatter). This file is the index —
> read the relevant doc before changing a component.

## 🚨 Read-me-first invariants

- **Apps must work offline.** Everything an app needs lives in its `www/` (plus the copied
  `www/shared/`). No CDN links, no external fonts — Capacitor packages `www/` onto the device as-is.
- **Never edit `apps/*/www/shared/`.** It is a generated copy of `shared/web/assets/`, overwritten
  on every build and git-ignored. Fix the source in `shared/`, never the copy.
- **Code that two or more apps need belongs in `shared/`**, never duplicated per app.
- **Never commit keystores or signing credentials** (`.gitignore` blocks `*.keystore`/`*.jks` — keep
  it that way).
- **EatWise data is precious, the app is disposable.** Never break the `{entries, analysis}` data
  format; strict semver + storage-key rules in [Knowledge/eatwise.md](Knowledge/eatwise.md).
- **Exchanges with Thomas are in French** — direct and concise. Each app's code-comment and UI
  language follows its own rules doc.
- **Fragile core:** touching `apps/eatwise/www/index.html` → run `scripts/verify.sh` before
  committing (the pre-commit hook blocks on it).

## 🔁 Development & verification

Test in the browser first (`npm run dev <app>`), deploy to a device (`npm run deploy <app>`) to
verify native behaviour. The fragile core is `apps/eatwise/www/index.html`: its business logic
(4h bloating window, D-1/D-2 pain correlation, import/export compatibility) is exactly where a fix
for one case silently breaks another. `scripts/verify.sh` runs the golden-file regression plus the
doc/plan rot-guards; the pre-commit hook (installed via `scripts/bootstrap.sh`) blocks any commit
that stages the fragile core without passing the goldens. Golden-baseline updates are deliberate
and need explicit human sign-off.

Before large or destructive changes (deleting an app, rewriting shared scripts), state the plan and
get confirmation.

## 📁 Repo map

| Path | Role |
|------|------|
| `apps/<name>/www/` | The app's web code — **this is where app work happens** |
| `apps/<name>/CLAUDE.md` | Pointer to the app's rules doc in `Knowledge/` — read it before touching the app |
| `apps/<name>/capacitor.config.json` | App id, display name, web dir |
| `apps/<name>/android/` | Generated native project (committed; only touch for permissions/icons/splash) |
| `shared/scripts/` | Build tooling shared by all apps (scaffold, dev, build, deploy) |
| `shared/web/assets/` | CSS/JS shared by all apps, copied to each app's `www/shared/` at build time |
| `scripts/` | Deterministic gates: rot-guards, verify gate, hooks, goldens |
| `Knowledge/` | The rulebook — one normative doc per component (index below) |
| `Plans/` | Roadmap — frontmatter is the source of truth; `Plans/README.md` is generated |
| `Bugs/` | Defect capture — `NNN_slug.md`, moved to `Bugs/Solved/` when closed |
| `.github/workflows/deploy-pages.yml` | Deploys `apps/eatwise/www/` to GitHub Pages on push to main |

## 📚 Knowledge index

| Doc | Open it when… |
|-----|---------------|
| [conventions.md](Knowledge/conventions.md) | …naming, app ids, git workflow, stack, origin legend |
| [runbook.md](Knowledge/runbook.md) | …you need an operational command (build, deploy, gates) |
| [setup.md](Knowledge/setup.md) | …first-time toolchain setup or connecting a phone |
| [eatwise.md](Knowledge/eatwise.md) | …touching anything under `apps/eatwise/` — data model, business logic, semver (in French) |
| [agentic-human-coexistence.md](Knowledge/agentic-human-coexistence.md) | …bootstrapping this structure in another repo, or asking why this one is shaped this way |

Doc taxonomy ("where do I put/find X?"): see the coexistence spec
[§4 table](Knowledge/agentic-human-coexistence.md).

## 🧬 Origin legend

| Class | Paths |
|-------|-------|
| Human-curated (agents never edit) | golden baselines under `scripts/goldens/` (updates need explicit sign-off), release keystores (never in git) |
| Generated-deterministic (never hand-edit) | `Plans/README.md` boards, `apps/*/www/shared/`, `apps/*/android/` cap-sync output |
| Source, human+agent co-edited | app code, `shared/`, `Knowledge/` docs (synced in the same commit as behaviour changes), `Plans/`, `Bugs/` |

## ⚠️ Gotchas — learned the hard way

- After every deploy that changes EatWise code, **bump the cache name in `sw.js`** — otherwise
  devices keep serving the old version.
- EatWise deliberately does **not** reference `shared/` — everything is inline in its `index.html`.

## ▶️ Run & test

```bash
npm run new-app <name> "<Display Name>"   # scaffold a new app
npm run dev <app>                         # serve www/ in the browser (quick iteration)
npm run build <app> [release]             # build APK
npm run deploy <app>                      # build debug APK + install via adb
scripts/verify.sh                         # THE gate: golden regression + doc/plan health
```

First-time setup (toolchain, hooks): [Knowledge/setup.md](Knowledge/setup.md) and
`scripts/bootstrap.sh`. Full command detail: [Knowledge/runbook.md](Knowledge/runbook.md).

<!-- bootstrapped from agentic-human-coexistence.md spec_version 1 -->
