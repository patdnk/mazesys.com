#!/bin/sh
# Renders design/og.html to public/og.png (1200 × 630) with a headless Chromium browser.
# Set BROWSER to override the browser binary.
set -e
cd "$(dirname "$0")/.."
BROWSER="${BROWSER:-/Applications/Brave Browser.app/Contents/MacOS/Brave Browser}"
"$BROWSER" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --window-size=1200,630 --virtual-time-budget=4000 \
  --screenshot="$PWD/public/og.png" "file://$PWD/design/og.html"
