import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("JUSTTCG_API_KEY")

url = "https://api.justtcg.com/v1/cards"
headers = {"x-api-key": api_key}
params = {
    "game": "pokemon",
    "set": "me-30th-celebration-pokemon",
    "orderBy": "price",
    "order": "desc",
    "limit": 10,
    "priceHistoryDuration": "30d",
    "condition": "NM",
}

response = requests.get(url, headers=headers, params=params, timeout=30)
print("Status:", response.status_code)

if response.status_code != 200:
    print(response.text)
    exit()

data = response.json()["data"]
print("Cards returned:", len(data))

if data:
    print("First card:", data[0]["name"])
    print("Its conditions:", [v["condition"] for v in data[0]["variants"]])

for card in data:
    for v in card["variants"]:
        if v["condition"] == "Near Mint":
            history = v.get("priceHistory") or []
            print("\n" + card["name"], "|", card.get("rarity"), "|", v.get("printing"), "| $", v["price"])
            print("History points:", len(history))
            if history:
                dates = [datetime.fromtimestamp(point["t"]).date() for point in history]
                print("History covers", min(dates), "to", max(dates))
