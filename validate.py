import glob
import json
import sys

for file in glob.glob("./animes/**/*.json"):
    data = json.load(open(file, "rb"))
    if data["data"]["mal_id"]:
        print(f"{file} is safe")
    else:
        print(f"{file} has errors")
        sys.exit()
