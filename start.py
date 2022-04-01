import os
import time
import json
from _request import session

ANIME_DIR = os.path.join(os.getcwd(), "animes")
ANIME_NO = 0

# {
#     "status": "429",
#     "type": "RateLimitException",
#     "message": "You are being rate-limited. Please follow Rate Limiting guidelines: https://jikan.docs.apiary.io/#introduction/information/rate-limiting",
#     "error": None,
# }
while True:
    BASE_DIR = f"{ANIME_DIR}\\{ANIME_NO}"
    res = session.get(f"https://api.jikan.moe/v4/anime/{ANIME_NO}")
    data = res.json()

    if (
        res.status_code == 200
        and data.get("status", None) != 404
        and data.get("status", None) != "429"
    ):
        file = open(f"{BASE_DIR}.json", "w+")
        json.dump(data, file, indent=4)
        file.close()
        print(f"Got Info for {ANIME_NO}")

    else:
        print(f"Missed info for {ANIME_NO}")

    time.sleep(1.2)

    ANIME_NO += 1
