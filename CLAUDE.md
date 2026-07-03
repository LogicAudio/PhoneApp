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

<!-- Thomas: paste your directives for how agents should work in this repo below. -->

- Before large or destructive changes (deleting an app, rewriting shared scripts), state the plan and get confirmation.

## Current apps

- **eatwise** — EatWise, nutrition app. Originated as a single HTML file from a claude.ai conversation.
