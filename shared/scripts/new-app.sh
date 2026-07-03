#!/usr/bin/env bash
# Scaffold a new Capacitor app under apps/<name>.
# Usage: shared/scripts/new-app.sh <name> "<Display Name>"
#   <name>          lowercase, no spaces (folder + package id segment)
#   <Display Name>  optional; shown under the app icon (defaults to <name>)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
NAME="${1:?usage: new-app.sh <name> \"<Display Name>\"}"
DISPLAY="${2:-$NAME}"
APP_DIR="$ROOT/apps/$NAME"
APP_ID="net.transpose.$NAME"

if [[ ! "$NAME" =~ ^[a-z][a-z0-9]*$ ]]; then
  echo "error: name must be lowercase letters/digits, starting with a letter (got '$NAME')" >&2
  exit 1
fi
[ -e "$APP_DIR" ] && { echo "error: apps/$NAME already exists" >&2; exit 1; }

mkdir -p "$APP_DIR/www"

cat > "$APP_DIR/package.json" <<EOF
{
  "name": "$NAME",
  "private": true,
  "version": "0.1.0",
  "dependencies": {
    "@capacitor/android": "^8.4.1",
    "@capacitor/core": "^8.4.1"
  },
  "devDependencies": {
    "@capacitor/cli": "^8.4.1"
  }
}
EOF

cat > "$APP_DIR/capacitor.config.json" <<EOF
{
  "appId": "$APP_ID",
  "appName": "$DISPLAY",
  "webDir": "www"
}
EOF

cat > "$APP_DIR/www/index.html" <<EOF
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>$DISPLAY</title>
  <link rel="stylesheet" href="shared/base.css">
</head>
<body>
  <main>
    <h1>$DISPLAY</h1>
    <p>New app scaffold — replace this with the real app.</p>
  </main>
</body>
</html>
EOF

echo "Installing dependencies..."
(cd "$ROOT" && npm install)

echo "Adding Android platform..."
(cd "$APP_DIR" && npx cap add android)

echo ""
echo "Created apps/$NAME (appId: $APP_ID)"
echo "Next: edit apps/$NAME/www/, then 'npm run deploy $NAME' to install on a device."
