#!/bin/bash

mkdir -p ~/.cache/vinyl

osascript << 'APPLESCRIPT'
set artPath to (POSIX path of (path to home folder)) & ".cache/vinyl/current_art.jpg"
tell application "Music"
    set trackArtwork to raw data of artwork 1 of current track
    set artFile to open for access POSIX file artPath with write permission
    set eof artFile to 0
    write trackArtwork to artFile
    close access artFile
end tell
APPLESCRIPT
