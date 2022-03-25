import os
import time
import json
import requests
from requests.adapters import HTTPAdapter, Retry

ANIME_DIR = os.path.join(os.getcwd(), "animes")
ANIME_NO = 51367

session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=0.1,
    status_forcelist=[
        429,
        400,
    ],
)

session.mount("http://", HTTPAdapter(max_retries=retries))


while True:
    res = session.get(f"https://api.jikan.moe/v4/anime/{ANIME_NO}")
    data = res.json()

    if res.status_code == 200 and data.get("status", None) != 404:
        BASE_DIR = f"{ANIME_DIR}\\{ANIME_NO}"
        os.makedirs(BASE_DIR) if not os.path.isdir(BASE_DIR) else None
        file = open(f"{BASE_DIR}/anime.json", "w+")
        json.dump(data, file, indent=4)
        file.close()

        # EPISODE_DONE = 0
        # episodes = data["data"]["episodes"]
        # while episodes >= EPISODE_DONE:
        #     _res = requests.get(
        #         f"https://api.jikan.moe/v4/anime/{ANIME_NO}/episodes/{EPISODE_DONE}"
        #     )
        #     _data = _res.json()
        #     if _data.get("title", None) != "":
        #         os.makedirs(f"{BASE_DIR}\\episodes") if not os.path.isdir(
        #             f"{BASE_DIR}\\episodes"
        #         ) else None
        #         _file = open(f"{BASE_DIR}/episodes/{EPISODE_DONE}.json", "w+")
        #         json.dump(_data, _file, indent=4)
        #         _file.close()
        #         print(f"Got info for {ANIME_NO} | Episode {EPISODE_DONE}")
        #     else:
        #         print(f"Missed info for {ANIME_NO} | Episode {EPISODE_DONE}")
        #     time.sleep(1)

        #     EPISODE_DONE += 1

        print(f"Got Info for {ANIME_NO}")
    else:
        print(f"Missed info for {ANIME_NO}")
    ANIME_NO += 1
    time.sleep(1.2)
