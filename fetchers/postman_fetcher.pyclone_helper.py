# fetchers/postman_fetcher.py
import requests, os
from config import POSTMAN_API_KEY

def download_collection(uid, name):
    url = f"https://api.getpostman.com/collections/{uid}"
    resp = requests.get(url, headers={"X-Api-Key": POSTMAN_API_KEY})
    data = resp.json()
    path = os.path.join("postman_json", f"{name}.json")
    os.makedirs("postman_json", exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    return path
