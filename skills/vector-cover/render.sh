#!/usr/bin/env bash
# Render a vector-cover HTML file to a crisp PNG using headless Chrome.
# No remote-debugging port needed. This launches its own headless instance.
#
# Usage:  ./render.sh <input.html> <output.png> [WIDTH] [HEIGHT]
#   WIDTH/HEIGHT are the LOGICAL canvas size (default 1200x480).
#   Output is 2x that (scale factor 2) => 2400x960 by default.
set -euo pipefail

IN="${1:?usage: render.sh input.html output.png [W] [H]}"
OUT="${2:?usage: render.sh input.html output.png [W] [H]}"
W="${3:-1200}"
H="${4:-480}"

# absolute file:// url
case "$IN" in
  /*) URL="file://$IN" ;;
  *)  URL="file://$(cd "$(dirname "$IN")" && pwd)/$(basename "$IN")" ;;
esac

CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
[ -x "$CHROME" ] || CHROME="/Applications/Chromium.app/Contents/MacOS/Chromium"
[ -x "$CHROME" ] || CHROME="$(command -v google-chrome || command -v chromium || true)"
[ -x "$CHROME" ] || { echo "Chrome/Chromium not found"; exit 1; }

"$CHROME" --headless --disable-gpu --hide-scrollbars --default-background-color=00000000 \
  --force-device-scale-factor=2 \
  --window-size="${W},${H}" \
  --screenshot="$OUT" \
  "$URL" >/dev/null 2>&1

echo "wrote $OUT ($((W*2))x$((H*2)))"
