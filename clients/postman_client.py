# clients/postman_client.py
import requests
from config import POSTMAN_API_KEY

HEADERS = {"X-Api-Key": POSTMAN_API_KEY}

def list_collections():
    resp = requests.get("https://api.getpostman.com/collections", headers=HEADERS)
    resp.raise_for_status()
    return resp.json()["collections"]
