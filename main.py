import PTN
import os
from imdb import Cinemagoer
from functools import cache

"""
"title given from user": {
    "imdbID": ...,
    "Season": ...,  # optional
    "Episode": ...,  # optional
}
"""

SCAN_FOLDER = "./subtitles"
SUB_EXTS = (".srt", ".sub", ".ass", ".ssa", ".smi", ".txt")

@cache
def imdb_fetch(video_name):
    ia = Cinemagoer()
    out = ia.search_movie(video_name)
    if len(out) <= 0:
        return None
    out = out[0]
    if out["kind"] == "tv series":
        ia.update(out, "episodes")
    return out


def main():
    for root, dirs, files in os.walk(SCAN_FOLDER):
        for name in files:
            if not (name.endswith(SUB_EXTS)):
                continue
            metadata = PTN.parse(name)
            imdb_data = imdb_fetch(metadata["title"])
            if imdb_data is None:
                print(f"[skip] {os.path.join(root, name)}")
                continue

            print(metadata)
            print(imdb_data["episodes"])


if __name__ == "__main__":
    main()
