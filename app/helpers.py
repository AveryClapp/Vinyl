import subprocess


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


def get_artwork():
    subprocess.run(
        ["app/scripts/get_artwork.sh"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


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
