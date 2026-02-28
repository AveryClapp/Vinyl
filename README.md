# Vinyl

A live Apple Music overlay for macOS OBS.

## Setup

```
git clone https://github.com/AveryClapp/vinyl
cd vinyl
just run
```

Then in OBS, add a Browser Source → `http://127.0.0.1:17351/overlay`

## Auto-start on login

To have the server start automatically whenever you log in (no need to run it manually):

```
bash install_service.sh
```

This installs a launchd service that keeps the server running in the background.
Logs are written to `~/.cache/vinyl/server.log`.

To stop and remove:
```
launchctl unload ~/Library/LaunchAgents/com.vinyl.server.plist
rm ~/Library/LaunchAgents/com.vinyl.server.plist
```

## Requirements

- macOS
- Apple Music
- OBS
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- just (for manual runs)
