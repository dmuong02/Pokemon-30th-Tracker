import requests

url = "https://api.pokemontcg.io/v2/sets"
params = {"orderBy": "-releaseDate", "pageSize": 5}

response = requests.get(url, params=params, timeout=30)
print("Status:", response.status_code)

sets = response.json()["data"]

for s in sets:
    print(s["id"], "|", s["name"], "|", s["releaseDate"], "|", s["total"], "cards")
    