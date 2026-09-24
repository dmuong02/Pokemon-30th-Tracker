import os
import json
import time

import requests

base = "https://api.tcgdex.net/v2/en"
set_ids = ["30th", "30th-c"]

all_cards = []

for set_id in set_ids:
    set_response = requests.get(base + "/sets/" + set_id, timeout=30)
    set_response.raise_for_status()
    card_list = set_response.json()["cards"]
    print(set_id, "|", len(card_list), "cards")

    for c in card_list:
        card_response = requests.get(base + "/cards/" + c["id"], timeout=30)
        card_response.raise_for_status()
        card = card_response.json()

        all_cards.append({
            "tcgdex_id": card["id"],
            "set_id": set_id,
            "local_id": card.get("localId"),
            "name": card.get("name"),
            "rarity": card.get("rarity"),
            "illustrator": card.get("illustrator"),
        })
        time.sleep(0.2)

os.makedirs("data/raw", exist_ok=True)
with open("data/raw/tcgdex_cards.json", "w") as f:
    json.dump(all_cards, f, indent=2)

print("\nSaved", len(all_cards), "cards")

for card in all_cards[:3] + all_cards[-3:]:
    print(card)