import subprocess

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from app.helpers import format_time, get_song_length, get_song_progress

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

    # Clean result into standard form
    if result.returncode != 0:
        return templates.TemplateResponse(request=request, name="base_state.html")

    response = result.stdout[:-1]
    if response == "Not playing":
        return templates.TemplateResponse(request=request, name="base_state.html")

    # Separate trackName and artistName
    response = list(response.split(":"))
    return templates.TemplateResponse(
        request=request, name="music_bar.html", context={"result": response}
    )


@app.get("/song/progress")
async def progress():
    cur_progress = get_song_progress()
    total_length = get_song_length()

    time_str = format_time(cur_progress)
    if cur_progress >= total_length:
        return Response(
            content=f"<span>{time_str}</span>",
            headers={"HX-Trigger": "song-finished"} 
        )

    return f'<span id="pblabel">{format_time(cur_progress)}</span>'


@app.get("/song/length")
async def length():
    return f'<span id="pblabel">{format_time(get_song_length())}</span>'

