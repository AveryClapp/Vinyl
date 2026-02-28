#!/bin/bash

osascript -e 'tell application "Music"
                set trackArtwork to raw data of artwork 1 of current track
                set fileName to ((path to desktop as text) & "current_art.jpg")
                set outFile to open for access file fileName with write permission
                set eof outFile to 0
                write trackArtwork to outFile
                close access outFile
            end tell'
