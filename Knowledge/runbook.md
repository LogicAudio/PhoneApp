---
name: runbook
type: runbook
governs:
  - shared/scripts/
read_when: You need an operational command — dev-serve, build, deploy, release, gates.
---

# Runbook

All commands run from the repo root. First-time toolchain setup: [setup.md](setup.md).

## Daily

```bash
npm run dev <app>            # serve www/ in the browser (quick iteration, no Android build)
npm run deploy <app>         # debug APK + install via adb on a USB-connected device
scripts/verify.sh            # THE gate: golden regression + doc/plan health
```

## Apps

```bash
npm run new-app <name> "<Display Name>"    # scaffold under apps/<name>
npm run build <app>                        # debug APK
npm run build <app> release                # release APK (needs signing config — never committed)
```

## PWA (EatWise)

Deployed automatically by `.github/workflows/deploy-pages.yml` on every push to `main` touching
`apps/eatwise/www/`. Production: https://logicaudio.github.io/PhoneApp/
After each deploy that changes code, bump the `sw.js` cache name — rule in [eatwise.md](eatwise.md).

## Gates & docs

```bash
scripts/bootstrap.sh                       # once per clone: git hooks + rot-guards
python3 scripts/check_knowledge.py         # doc rot-guard (--staged, --strict, --quiet)
python3 scripts/check_plans.py             # regenerate Plans/README.md boards (--check to gate)
node scripts/eatwise_golden.mjs            # fragile-core goldens (--update to re-baseline — deliberate, human sign-off)
```
