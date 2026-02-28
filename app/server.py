import os
import subprocess
from urllib.parse import quote as urlquote

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from app.helpers import (ARTWORK_PATH, format_time, get_artwork,
                         get_current_track, get_song_length, get_song_progress)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/overlay", response_class=HTMLResponse)
@app.get("/", response_class=HTMLResponse)
async def render(request: Request):
    SCRIPT_PATH = "app/scripts/get_song.sh"
    result = subprocess.run(
        [SCRIPT_PATH],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        return templates.TemplateResponse(request=request, name="base_state.html")

    response = result.stdout.strip()
    if response == "Not playing":
        return templates.TemplateResponse(request=request, name="base_state.html")

    song = list(response.split("|||", 1))
    get_artwork(song[0], song[1] if len(song) > 1 else "")

    cur_progress = get_song_progress()
    total_length = get_song_length()
    initial_pct = round((cur_progress / total_length) * 100, 1) if total_length > 0 else 0

    return templates.TemplateResponse(
        request=request,
        name="music_bar.html",
        context={
            "result": song,
            "track_encoded": urlquote(song[0]),
            "cur_progress": cur_progress,
            "total_length": total_length,
            "initial_pct": initial_pct,
        },
    )


@app.get("/song/artwork")
async def artwork():
    if not os.path.exists(ARTWORK_PATH):
        raise HTTPException(status_code=404)
    return FileResponse(
        ARTWORK_PATH,
        media_type="image/jpeg",
        headers={"Cache-Control": "no-store"},
    )


@app.get("/song/position")
async def song_position():
    current_track = get_current_track()
    cur_progress = get_song_progress()
    return {
        "playing": current_track is not None,
        "track": current_track or "",
        "position": cur_progress,
    }
