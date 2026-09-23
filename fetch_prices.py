import os
import json
import time
from datetime import date

import requests
from dotenv import load_dotenv

load_dotenv()


def fetch():
    api_key = os.getenv("JUSTTCG_API_KEY")

    url = "https://api.justtcg.com/v1/cards"
    headers = {"x-api-key": api_key}

    set_ids = [
        "me-30th-celebration-pokemon",
        "me-30th-celebration-classic-collection-pokemon",
    ]

    all_cards = []

    for set_id in set_ids:
        offset = 0
        has_more = True

        while has_more:
            params = {
                "game": "pokemon",
                "set": set_id,
                "condition": "NM",
                "priceHistoryDuration": "30d",
                "limit": 20,
                "offset": offset,
            }

            response = requests.get(url, headers=headers, params=params, timeout=30)

            if response.status_code != 200:
                print("Error on", set_id, "at offset", offset, "-", response.status_code)
                print(response.text)
                exit(1)

            body = response.json()
            cards = body["data"]
            all_cards.extend(cards)
            print(set_id, "| offset", offset, "| got", len(cards), "cards")

            has_more = body.get("meta", {}).get("hasMore", False)
            offset = offset + 20
            time.sleep(7)

    os.makedirs("data/raw", exist_ok=True)
    filename = "data/raw/justtcg_" + str(date.today()) + ".json"

    with open(filename, "w") as f:
        json.dump(all_cards, f, indent=2)

    print("\nSaved", len(all_cards), "cards to", filename)
    return filename


if __name__ == "__main__":
    fetch()