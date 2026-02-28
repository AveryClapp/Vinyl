#!/bin/bash

mkdir -p "$HOME/.cache/vinyl"
ARTWORK_PATH="$HOME/.cache/vinyl/current_art.jpg"

osascript << EOF
tell application "Music"
    set trackArtwork to raw data of artwork 1 of current track
    set artFile to open for access POSIX file "$ARTWORK_PATH" with write permission
    set eof artFile to 0
    write trackArtwork to artFile
    close access artFile
end tell
EOF
