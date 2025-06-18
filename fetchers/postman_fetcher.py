# fetchers/postman_fetcher.py

import os
import json
import requests
from config import POSTMAN_API_KEY

def download_collection(uid: str, name: str) -> str:
    """
    Downloads the Postman collection JSON for the given UID and
    saves it locally under postman_json/{name}.json, returning the path.
    """
    url = f"https://api.getpostman.com/collections/{uid}"
    headers = {"X-Api-Key": POSTMAN_API_KEY}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    os.makedirs("postman_json", exist_ok=True)
    path = os.path.join("postman_json", f"{name}.json")

    with open(path, "w") as f:
        json.dump(resp.json(), f, indent=2)

    return path
