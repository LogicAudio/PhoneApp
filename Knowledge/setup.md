---
name: setup
type: runbook
governs:
  - shared/scripts/env.sh
read_when: First-time toolchain setup (Java, Android SDK, adb), connecting a phone, or driving this repo from the Claude mobile app.
---

# Setup

## Toolchain (macOS)

Everything installs via Homebrew — no Android Studio required:

```bash
brew install openjdk@21                                        # Java for Gradle
brew install --cask android-commandlinetools android-platform-tools   # SDK manager + adb

# Accept licenses and install SDK packages
SDK_ROOT="$(brew --prefix)/share/android-commandlinetools"
export JAVA_HOME="$(brew --prefix openjdk@21)/libexec/openjdk.jdk/Contents/Home"
yes | "$SDK_ROOT/cmdline-tools/latest/bin/sdkmanager" --licenses --sdk_root="$SDK_ROOT"
"$SDK_ROOT/cmdline-tools/latest/bin/sdkmanager" --sdk_root="$SDK_ROOT" \
  "platform-tools" "platforms;android-35" "build-tools;35.0.0"
```

The build scripts (`shared/scripts/env.sh`) resolve `JAVA_HOME` and `ANDROID_HOME` from these Homebrew locations automatically, so no `.zshrc` changes are needed. If you install Java/SDK elsewhere, export `JAVA_HOME`/`ANDROID_HOME` yourself.

Then install JS dependencies:

```bash
npm install
```

## Installing an app on your phone

1. On the phone: Settings → About phone → tap **Build number** 7 times, then Settings → Developer options → enable **USB debugging**.
2. Plug the phone into the Mac via USB, accept the "Allow USB debugging?" prompt.
3. `npm run deploy eatwise`

## Working from your phone (Claude Remote Control)

To drive a Claude Code session on this Mac from the Claude mobile app:

1. On the Mac, in a terminal at the repo root: `claude remote-control --name "PhoneApp"`
   (or run `/remote-control PhoneApp` inside an existing Claude Code session).
2. In the Claude mobile app: tap **Code** in the navigation, pick the "PhoneApp" session (green dot = online), or scan the QR code the Mac shows (press spacebar).
3. Requires a Pro/Max/Team account signed in on both ends, Claude Code ≥ 2.1.51, and the Mac process left running.

Note: the mobile app cannot upload files from the phone's storage into the session. To bring in content from a claude.ai conversation (e.g. an artifact), publish the artifact (share icon → publish → copy link) and paste the link into the session — Claude can fetch it from there.
