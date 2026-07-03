# PhoneApp — instructions for AI agents

Monorepo of Android apps built with Capacitor. Each app is plain web code (HTML/CSS/JS in `apps/<name>/www/`) wrapped into a native Android app. Android-first, iOS-ready.

## Repository map

- `apps/<name>/www/` — the app's web code. **This is where app work happens.**
- `apps/<name>/capacitor.config.json` — app id, display name, web dir.
- `apps/<name>/android/` — generated native project. Committed, but only touch it for native concerns (permissions in `AndroidManifest.xml`, icons, splash screens).
- `shared/scripts/` — tooling shared by all apps (scaffold, build, deploy). Fix bugs here once, never copy scripts into apps.
- `shared/web/assets/` — CSS/JS shared by all apps. Build/dev scripts copy it to each app's `www/shared/` (that copy is generated — never edit it; it is overwritten on every build).
- `docs/SETUP.md` — toolchain setup and device/phone connection.

## Commands (run from repo root)

- `npm run new-app <name> "<Display Name>"` — scaffold a new app
- `npm run dev <app>` — serve an app's `www/` in the browser (quick iteration, no Android build)
- `npm run build <app> [release]` — build APK
- `npm run deploy <app>` — build debug APK + install on USB-connected device via adb

## Conventions

- App ids: `net.transpose.<name>`. App folder names: lowercase, no spaces.
- Apps must work offline: everything an app needs lives in its `www/` (plus the copied `www/shared/`). No CDN links, no external fonts — Capacitor packages `www/` onto the device as-is.
- Code that two or more apps need belongs in `shared/`, not duplicated per app.
- Test in the browser first (`npm run dev`), deploy to device to verify native behavior.
- Never commit keystores or signing credentials.

## Agent directives

- **Exchanges with Thomas are in French** — direct and concise. Code comments and app UI language follow each app's own CLAUDE.md.
- Each app can have its own `apps/<name>/CLAUDE.md` with app-specific directives (data model, business logic, versioning rules). **Read it before touching that app** — it takes precedence over generic conventions here.
- Before large or destructive changes (deleting an app, rewriting shared scripts), state the plan and get confirmation.

## Current apps

- **eatwise** — EatWise, personal health-tracking app (digestion + spondylarthritis pain), in French. A single self-contained `index.html` (vanilla JS, no build, no CDN — deliberate). Current phase: installable PWA deployed via GitHub Pages; the Capacitor/APK wrapper is secondary. Detailed directives: `apps/eatwise/CLAUDE.md` — read it first, it has strict data-compatibility and semver rules.
