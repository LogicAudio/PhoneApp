# PhoneApp

Monorepo for Android mobile apps built with [Capacitor](https://capacitorjs.com): each app is plain web code (HTML/CSS/JS) wrapped into a native Android app. Structured Android-first but iOS-ready (Capacitor supports adding an `ios/` platform per app later).

## Layout

```
apps/            One folder per app
  eatwise/       EatWise — first app
    www/         The app's web code (HTML/CSS/JS) — this is what you edit
    android/     Generated native Android project (committed, rarely touched)
    capacitor.config.json
shared/
  scripts/       Shared tooling: scaffold, build, deploy
  web/           Shared web assets (CSS/JS) copied into every app at build time
docs/            Setup and workflow documentation
CLAUDE.md        Instructions and directives for AI agents working in this repo
```

## Common commands

Run from the repo root:

| Command | What it does |
|---|---|
| `npm run new-app <name> "<Display Name>"` | Scaffold a new app under `apps/<name>` |
| `npm run dev <app>` | Serve an app's `www/` in the browser for quick iteration |
| `npm run build <app>` | Build a debug APK |
| `npm run build <app> release` | Build a release APK |
| `npm run deploy <app>` | Build and install on a USB-connected Android device |

## First-time setup

See [docs/SETUP.md](docs/SETUP.md) for toolchain installation (Java, Android SDK, adb) and how to connect a phone.
