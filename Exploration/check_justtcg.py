import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("JUSTTCG_API_KEY")

url = "https://api.justtcg.com/v1/sets"
headers = {"x-api-key": api_key}
params = {"game": "pokemon", "q": "30th"}

response = requests.get(url, headers=headers, params=params, timeout=30)
print("Status:", response.status_code)

if response.status_code != 200:
    print(response.text)
    exit()

for s in response.json()["data"]:
    print(s["id"], "|", s["name"], "|", s.get("release_date"), "|", s.get("set_value_usd"))