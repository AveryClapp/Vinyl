import subprocess


def format_time(time):
    minutes = time // 60
    seconds = time % 60
    if seconds < 10:
        return f'{minutes}:0{seconds}'
    return f'{minutes}:{seconds}'

def get_song_progress():
    PROGRESS_PATH = "app/scripts/song_progress.sh"
    progress_result = subprocess.run(
        [PROGRESS_PATH],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


    # Clean result into standard form
    if progress_result.returncode != 0:
        return 0

    response = progress_result.stdout[:-1]

    cur_time = int(response.split(".")[0])
    cur_time = round(cur_time, 0)
    return cur_time

def get_song_length():
    LENGTH_PATH = "app/scripts/song_length.sh"
    length_result = subprocess.run(
        [LENGTH_PATH],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Clean result into standard form
    if length_result.returncode != 0:
        return 0

    response = length_result.stdout[:-1]

    total_time = int(response.split(".")[0])
    total_time = round(total_time, 0)
    return total_time
