import os
import time
import json
import requests
from requests.adapters import HTTPAdapter, Retry

ANIME_DIR = os.path.join(os.getcwd(), "animes")
ANIME_NO = 0

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
        character_res = session.get(
            f"https://api.jikan.moe/v4/anime/{ANIME_NO}/characters"
        )
        character_data = character_res.json()
        time.sleep(1)

        if character_res.status_code == 200 and len(character_data.get("data", {})) > 0:
            data["data"]["characters"] = character_data.get("data", [])

            if (
                not data["data"]["characters"] == character_data["data"]
                or character_data.get("status", "") == "429"
            ):
                print(f"Error in {ANIME_NO} | Characters")
                break

        relation_res = session.get(
            f"https://api.jikan.moe/v4/anime/{ANIME_NO}/relations"
        )
        relation_data = relation_res.json()
        time.sleep(1)

        if relation_res.status_code == 200 and len(relation_data.get("data", {})) > 0:
            data["data"]["relations"] = relation_data.get("data", [])

            if (
                not data["data"]["relations"] == relation_data.get("data", [])
                or relation_data.get("status", "") == "429"
            ):
                print(f"Error in {ANIME_NO} | Relations")
                break

        more_info_res = session.get(
            f"https://api.jikan.moe/v4/anime/{ANIME_NO}/moreinfo"
        )
        more_info_data = more_info_res.json()
        time.sleep(1)

        if more_info_res.status_code == 200 and len(more_info_data.get("data", {})) > 0:
            data["data"]["moreinfo"] = more_info_data["data"].get("moreinfo", [])

            if (
                not data["data"]["moreinfo"]
                == more_info_data["data"].get("moreinfo", [])
                or more_info_data.get("status", "") == "429"
            ):
                print(f"Error in {ANIME_NO} | More Info")
                break

        recommendation_res = session.get(
            f"https://api.jikan.moe/v4/anime/{ANIME_NO}/recommendations"
        )
        recommendation_data = recommendation_res.json()
        time.sleep(1)

        if (
            recommendation_res.status_code == 200
            and len(recommendation_data.get("data", {})) > 0
        ):
            data["data"]["recommendations"] = recommendation_data.get("data", [])

            if (
                not data["data"]["recommendations"]
                == recommendation_data.get("data", [])
                or recommendation_data.get("status", "") == "429"
            ):
                print(f"Error in {ANIME_NO} | Recommendations")
                break

        file = open(f"{BASE_DIR}.json", "w+")
        json.dump(data, file, indent=4)
        file.close()
        time.sleep(1.5)
        print(f"Got Info for {ANIME_NO}")

    else:
        time.sleep(1.2)
        print(f"Missed info for {ANIME_NO}")
    ANIME_NO += 1
