import json
import os
import subprocess
from urllib.parse import quote as urlquote
from urllib.request import urlopen, urlretrieve

ARTWORK_PATH = os.path.expanduser("~/.cache/vinyl/current_art.jpg")


def format_time(time):
    time = int(time)
    minutes = time // 60
    seconds = time % 60
    return f'{minutes}:{seconds:02d}'


def get_current_track():
    result = subprocess.run(
        ["app/scripts/get_song.sh"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        return None

    response = result.stdout.strip()
    if response == "Not playing":
        return None

    return response.split(":")[0]


def get_artwork(track: str, artist: str):
    os.makedirs(os.path.dirname(ARTWORK_PATH), exist_ok=True)
    query = urlquote(f"{track} {artist}")
    url = f"https://itunes.apple.com/search?term={query}&media=music&entity=song&limit=1"
    try:
        with urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read())
        if data["resultCount"] > 0:
            img_url = data["results"][0]["artworkUrl100"].replace("100x100bb", "600x600bb")
            urlretrieve(img_url, ARTWORK_PATH)
    except Exception:
        pass


def get_song_progress():
    result = subprocess.run(
        ["app/scripts/song_progress.sh"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        return 0

    return int(result.stdout.strip().split(".")[0])


def get_song_length():
    result = subprocess.run(
        ["app/scripts/song_length.sh"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        return 0

    return int(result.stdout.strip().split(".")[0])
