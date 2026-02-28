#!/bin/bash

osascript -e 'tell application "Music"
                if player state is playing then
                    set artistName to artist of current track
                    set trackName to name of current track
                    return trackName & ":" & artistName
                else
                    return "Not playing"
                end if
              end tell'
