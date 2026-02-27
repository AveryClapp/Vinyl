import os
import subprocess

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    # Base case... empty
    return {"message": ""}

@app.get("/overlay")
async def render():
    # Render page that gets song name and artist

    # Get required information
    SCRIPT_PATH = "app/get_song.sh"
    result = subprocess.run([SCRIPT_PATH], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result

