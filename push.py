import json
import sys
import requests
import ast
import os

BASEURL = "http://127.0.0.1:8000/api/v1/anime/"
AUTH_TOKEN = {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0ODYyMTgxNSwiaWF0IjoxNjQ4NTM1NDE1LCJqdGkiOiI3ODA5OGZkZjYyNmE0ODEwODUyNDIzYTJkODIxMGRmMSIsInVzZXJfaWQiOjF9.Dp5jrjtO1wyksnOmTccVXOaqBnYshPsX-mW0DCIh8zU",
}


def main(file):
    access_request = requests.post(
        "http://127.0.0.1:8000/api/v1/token/refresh/",
        json={
            "refresh": AUTH_TOKEN["refresh"],
        },
    )
    access = ast.literal_eval(access_request.text)["access"]
    data = json.load(open(file, "rb"))["data"]
    image_url = data["images"]["webp"]["image_url"]
    anime_cover = requests.get(image_url)

    DATA = {
        "episodes": [],
        "mal_id": data["mal_id"],
        "anime_name": data["title"],
        "anime_name_japanese": data["title_japanese"],
        "anime_source": data["source"],
        "anime_aired_from": data["aired"]["from"],
        "anime_aired_to": data["aired"]["to"],
        "anime_synopsis": data["synopsis"],
        "anime_background": data["background"],
        "anime_rating": data["rating"],
        "anime_genres": data["genres"],
        "anime_themes": data["themes"],
        "anime_studios": data["studios"],
        "anime_producers": data["producers"],
        "anime_name_synonyms": [],
    }

    for item in data["title_synonyms"]:
        DATA["anime_name_synonyms"].append({"name": item})

    res = requests.post(
        BASEURL,
        json=DATA,
        headers={
            "authorization": f"Bearer {access}",
        },
    )

    # print(json.dumps(DATA, indent=5))

    if anime_cover.status_code == 200:
        image_res = requests.put(
            f"{BASEURL}{res.json()['id']}/",
            data=DATA,
            files={
                "anime_cover": (f"{data['mal_id']}.webp", anime_cover.content),
            },
            headers={
                "authorization": f"Bearer {access}",
            },
        )
        if image_res.status_code != 200:
            print(f"Cannot push {data['mal_id']} | Status {image_res.status_code}")

            with open("image_res.html", "w", encoding="utf-8") as f:
                f.write(image_res.text)

            sys.exit()
    else:
        file = open("broken.txt", "a+")
        file.write(f'MAL ID = {data["mal_id"]} | Primary Key = {res.json()["id"]}\n')

    if res.status_code == 201:
        print(f"PUSHED {data['mal_id']}")
    else:
        print(f"Cannot push {data['mal_id']} | Status {res.status_code}")
        with open("res.html", "w", encoding="utf-8") as f:
            f.write(res.text)

        sys.exit()


def list_full_paths(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory)]


if __name__ == "__main__":
    full_dir = sorted(list_full_paths("./animes"))
    for files in full_dir:
        main(files)
