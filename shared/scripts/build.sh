#!/usr/bin/env bash
# Build an APK for an app.
# Usage: shared/scripts/build.sh <app-name> [debug|release]   (default: debug)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
source "$ROOT/shared/scripts/env.sh"

APP="${1:?usage: build.sh <app-name> [debug|release]}"
VARIANT="${2:-debug}"
APP_DIR="$ROOT/apps/$APP"

[ -d "$APP_DIR" ] || { echo "error: no such app: apps/$APP" >&2; exit 1; }

# Copy shared web assets into the app so they get packaged by `cap sync`
if [ -d "$ROOT/shared/web/assets" ]; then
  mkdir -p "$APP_DIR/www/shared"
  rsync -a --delete "$ROOT/shared/web/assets/" "$APP_DIR/www/shared/"
fi

cd "$APP_DIR"
npx cap sync android

cd android
case "$VARIANT" in
  debug)   ./gradlew assembleDebug ;;
  release) ./gradlew assembleRelease ;;
  *) echo "error: unknown variant '$VARIANT' (use debug or release)" >&2; exit 1 ;;
esac

APK="$(ls "$APP_DIR"/android/app/build/outputs/apk/"$VARIANT"/*.apk 2>/dev/null | head -1)"
echo ""
echo "APK built: $APK"
