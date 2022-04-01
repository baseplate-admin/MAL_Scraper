import json
import sys
import time
from _request import session
import os

from natsort import natsorted

DIRECTORY = "./animes"
DUMP_DIR = "./characters"
FILES = natsorted(set(os.listdir(DIRECTORY)) - set(os.listdir(DUMP_DIR)))

for file in FILES:
    json_data = json.load(open(os.path.join(DIRECTORY, file), "r", encoding="utf-8"))
    mal_id = json_data["data"]["mal_id"]

    res = session.get(f"https://api.jikan.moe/v4/anime/{mal_id}/characters")
    json_data["data"]["characters"] = res.json().get("data")

    json.dump(
        json_data, open(f"{DUMP_DIR}/{mal_id}.json", "w+", encoding="utf-8"), indent=4
    )
    time.sleep(1.2)

    # Validation
    if json.load(
        open(os.path.join(DIRECTORY, file), "r", encoding="utf-8")
    ) == json.load(open(f"{DUMP_DIR}/{mal_id}.json", "r", encoding="utf-8")):
        sys.exit()
    else:
        print(f"Got Character info for {mal_id}")
