#!/usr/bin/env bash
# Build a debug APK and install it on a USB-connected Android device.
# Usage: shared/scripts/deploy.sh <app-name>
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
source "$ROOT/shared/scripts/env.sh"

APP="${1:?usage: deploy.sh <app-name>}"

"$ROOT/shared/scripts/build.sh" "$APP" debug

if ! adb get-state >/dev/null 2>&1; then
  echo "error: no Android device detected. Plug in via USB and enable USB debugging" >&2
  echo "(Settings > About phone > tap 'Build number' 7x, then Developer options > USB debugging)" >&2
  exit 1
fi

APK="$ROOT/apps/$APP/android/app/build/outputs/apk/debug/app-debug.apk"
adb install -r "$APK"
echo "Installed $APP on device."
