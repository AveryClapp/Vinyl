import os
import subprocess

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from app.helpers import format_time, get_artwork, get_song_length, get_song_progress

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/overlay", response_class=HTMLResponse)
@app.get("/", response_class=HTMLResponse)
async def render(request: Request):
    SCRIPT_PATH = "app/scripts/get_song.sh"
    result = subprocess.run(
        [SCRIPT_PATH],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        return templates.TemplateResponse(request=request, name="base_state.html")

    response = result.stdout.strip()
    if response == "Not playing":
        return templates.TemplateResponse(request=request, name="base_state.html")

    get_artwork()

    song = list(response.split(":"))
    return templates.TemplateResponse(
        request=request, name="music_bar.html", context={"result": song}
    )


@app.get("/song/artwork")
async def artwork():
    artwork_path = os.path.expanduser("~/.cache/vinyl/current_art.jpg")
    if not os.path.exists(artwork_path):
        raise HTTPException(status_code=404)
    return FileResponse(
        artwork_path,
        media_type="image/jpeg",
        headers={"Cache-Control": "no-store"},
    )


@app.get("/song/progress")
async def progress():
    cur_progress = get_song_progress()
    total_length = get_song_length()

    percent = min((cur_progress / total_length) * 100, 100) if total_length > 0 else 0

    fragment = f"""
<div class="progress-track">
  <div class="progress-fill" style="width: {percent:.1f}%;"></div>
</div>
<div class="time-row">
  <span>{format_time(cur_progress)}</span>
  <span>{format_time(total_length)}</span>
</div>"""

    if cur_progress >= total_length and total_length > 0:
        return Response(
            content=fragment,
            media_type="text/html",
            headers={"HX-Trigger": "song-finished"},
        )

    return HTMLResponse(content=fragment)
