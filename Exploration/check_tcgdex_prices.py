import requests

base = "https://api.tcgdex.net/v2/en"

set_response = requests.get(base + "/sets/30th", timeout=30)
print("Set status:", set_response.status_code)

if set_response.status_code != 200:
    print("API error, try again in a minute.")
    exit()

cards = set_response.json()["cards"]
print("Cards in set:", len(cards))

sample = cards[:2] + cards[-2:]

for c in sample:
    card_response = requests.get(base + "/cards/" + c["id"], timeout=30)
    card = card_response.json()
    print("\n" + card["name"], "|", card.get("rarity"))
    print(card.get("pricing"))