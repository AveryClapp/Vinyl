#!/bin/bash

set -e

VINYL_DIR="$(cd "$(dirname "$0")" && pwd)"
UV_PATH="$(which uv 2>/dev/null || echo "")"
PLIST="$HOME/Library/LaunchAgents/com.vinyl.server.plist"
LOG_DIR="$HOME/.cache/vinyl"

if [ -z "$UV_PATH" ]; then
  echo "Error: uv not found in PATH. Install it first: https://docs.astral.sh/uv/getting-started/installation/"
  exit 1
fi

mkdir -p "$LOG_DIR"

cat > "$PLIST" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.vinyl.server</string>
    <key>ProgramArguments</key>
    <array>
        <string>${UV_PATH}</string>
        <string>run</string>
        <string>fastapi</string>
        <string>run</string>
        <string>app/server.py</string>
        <string>--port</string>
        <string>17351</string>
    </array>
    <key>WorkingDirectory</key>
    <string>${VINYL_DIR}</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>${LOG_DIR}/server.log</string>
    <key>StandardErrorPath</key>
    <string>${LOG_DIR}/server.log</string>
</dict>
</plist>
EOF

# Unload first in case it was already installed
launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"

echo "Vinyl service installed. Starts automatically on login."
echo "Logs: $LOG_DIR/server.log"
echo ""
echo "To stop:      launchctl unload $PLIST"
echo "To uninstall: launchctl unload $PLIST && rm $PLIST"
