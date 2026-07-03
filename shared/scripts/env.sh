# Sourced by build/deploy scripts — resolves the Java and Android SDK locations.
# Values already exported in your shell take precedence.
BREW_PREFIX="$(brew --prefix 2>/dev/null || echo /usr/local)"

export JAVA_HOME="${JAVA_HOME:-$BREW_PREFIX/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home}"
export ANDROID_HOME="${ANDROID_HOME:-$BREW_PREFIX/share/android-commandlinetools}"
export PATH="$ANDROID_HOME/platform-tools:$JAVA_HOME/bin:$PATH"

if [ ! -d "$JAVA_HOME" ]; then
  echo "warning: JAVA_HOME not found at $JAVA_HOME — see docs/SETUP.md" >&2
fi
if [ ! -d "$ANDROID_HOME" ]; then
  echo "warning: ANDROID_HOME not found at $ANDROID_HOME — see docs/SETUP.md" >&2
fi
