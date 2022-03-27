from email.mime import image
import json
import sys
import requests
import ast
import os

BASEURL = "http://127.0.0.1:8000/api/v1/anime/"
AUTH_TOKEN = {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0ODQ3MDQyMywiaWF0IjoxNjQ4Mzg0MDIzLCJqdGkiOiI0ZWE1ZGI4YWE3M2M0NmUyYTZlMDU1MjExY2NlNzJjNiIsInVzZXJfaWQiOjF9.SunZ_F2Fa8Lv-on4BUwuJZRQ5MnYtQSoUtKxevAYaxk",
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
    anime_cover = requests.get(image_url).content

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
    }
    res = requests.post(
        BASEURL,
        json=DATA,
        headers={
            "authorization": f"Bearer {access}",
        },
    )
    if anime_cover:
        image_res = requests.put(
            f"{BASEURL}{data['mal_id']}/",
            data=DATA,
            files={
                "anime_cover": (f"{data['mal_id']}.webp", anime_cover),
            },
            headers={
                "authorization": f"Bearer {access}",
            },
        )
    else:
        file = open("broken.json", "w+")
        data = json.load(file)
        data.append(
            {"episode": data["mal_id"]},
        )
        json.dump(
            data,
            file,
            indent=4,
        )

    if res.status_code == 201:
        print(f"PUSHED {data['mal_id']}")
    else:
        print(f"Cannot push {data['mal_id']} | Status {res.status_code}")
        with open("res.html", "w", encoding="utf-8") as f:
            f.write(res.text)
        with open("image_res.html", "w", encoding="utf-8") as f:
            f.write(image_res.text)
        sys.exit()


def list_full_paths(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory)]


if __name__ == "__main__":
    full_dir = sorted(list_full_paths("./animes"))
    for files in full_dir:
        main(files)
    # first_list = full_dir[range * 0 : range]
    # second_list = full_dir[(range * 1) + 1 : range * 2]
    # third_list = full_dir[(range * 2) + 1 : range * 3]
    # fourth_list = full_dir[(range * 3) + 1 : range * 4]
    # fifth_list = full_dir[(range * 4) + 1 : range * 5]
    # sixth_list = full_dir[(range * 5) + 1 : range * 6]
    # sventh_list = full_dir[(range * 6) + 1 : range * 7]
    # eighth_list = full_dir[(range * 7) + 1 : range * 8]
    # ninth_list = full_dir[(range * 8) + 1 : range * 9]
    # last_list = full_dir[(range * 9) + 1]

    # import threading
