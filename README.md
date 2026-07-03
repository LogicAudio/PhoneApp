# PhoneApp

Monorepo for Android mobile apps built with [Capacitor](https://capacitorjs.com): each app is
plain web code (HTML/CSS/JS) wrapped into a native Android app. Android-first, iOS-ready; apps
can also ship as PWAs via GitHub Pages. First app: **EatWise**, a personal health-tracking PWA.

**EatWise (PWA) en production : https://logicaudio.github.io/PhoneApp/** — déployée
automatiquement par GitHub Actions à chaque push touchant `apps/eatwise/www/`.

> **The canonical map is [CLAUDE.md](CLAUDE.md)** — the single index of what each part does
> and which rule file to open for detail. This README is just the front door, not a mirror.

## Quick start

```bash
npm install                 # once; toolchain setup: docs/SETUP.md
scripts/bootstrap.sh        # once per clone: git hooks + rot-guards
npm run dev eatwise         # serve the app in the browser
npm run deploy eatwise      # build APK + install on USB-connected device
```

Signing keystores are git-ignored — never commit credentials.
