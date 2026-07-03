#!/usr/bin/env bash
# Serve an app's www/ folder in the browser for quick iteration (no Android build).
# Usage: shared/scripts/dev.sh <app-name> [port]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
APP="${1:?usage: dev.sh <app-name> [port]}"
PORT="${2:-5173}"
APP_DIR="$ROOT/apps/$APP"

[ -d "$APP_DIR/www" ] || { echo "error: no such app: apps/$APP" >&2; exit 1; }

# Mirror shared assets so the browser sees the same thing the device will
if [ -d "$ROOT/shared/web/assets" ]; then
  mkdir -p "$APP_DIR/www/shared"
  rsync -a --delete "$ROOT/shared/web/assets/" "$APP_DIR/www/shared/"
fi

echo "Serving apps/$APP/www at http://localhost:$PORT"
npx --yes serve "$APP_DIR/www" -l "$PORT"
