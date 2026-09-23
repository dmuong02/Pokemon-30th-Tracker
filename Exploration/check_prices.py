import requests

url = "https://api.pokemontcg.io/v2/cards"
params = {
    "q": "set.id:me55",
    "pageSize": 250,
}

response = requests.get(url, params=params, timeout=60)
print("Status:", response.status_code)

if response.status_code != 200:
    print("API error, try again in a minute.")
    exit()


cards = response.json()["data"]
print("Cards returned:", len(cards))

with_prices = 0
for c in cards:
    if "tcgplayer" in c and "prices" in c["tcgplayer"]:
        with_prices = with_prices + 1

print("Cards with TCGplayer prices:", with_prices)

for c in cards[:5]:
    print(c["name"], "|", c.get("rarity"), "|", c.get("tcgplayer", {}).get("prices"))
