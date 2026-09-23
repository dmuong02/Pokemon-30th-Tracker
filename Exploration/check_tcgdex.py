import requests

url = "https://api.tcgdex.net/v2/en/sets"

response = requests.get(url, timeout=30)
print("Status:", response.status_code)

if response.status_code != 200:
    print("API error, try again in a minute.")
    exit()

sets = response.json()
print("Total sets:", len(sets))

for s in sets:
    if "30th" in s["name"]:
        print(s["id"], "|", s["name"], "|", s.get("cardCount", {}).get("total"), "cards")