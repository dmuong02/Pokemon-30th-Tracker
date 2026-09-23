import os
import json
import glob
from datetime import datetime, timezone

import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()


def load():
    # 1. Find the newest raw file
    latest_file = sorted(glob.glob("data/raw/justtcg_*.json"))[-1]
    print("Loading", latest_file)

    with open(latest_file) as f:
        raw_cards = json.load(f)

    # 2. Transform raw JSON into rows for each table
    sets = {}
    cards = []
    prices = {}

    for c in raw_cards:
        if c.get("rarity") == "Code Card":
            continue

        sets[c["set"]] = c["set_name"]

        if " - " in c["name"]:
            card_name, card_number = c["name"].rsplit(" - ", 1)
        else:
            card_name, card_number = c["name"], None

        v = c["variants"][0]
        cards.append((c["id"], c["set"], card_name, card_number,
                      c.get("rarity"), v.get("printing"), c.get("tcgplayerId")))

        for point in v.get("priceHistory") or []:
            price_date = datetime.fromtimestamp(point["t"], tz=timezone.utc).date()
            prices[(c["id"], price_date)] = point["p"]

    set_rows = []
    for set_id, set_name in sets.items():
        set_rows.append((set_id, set_name, "2026-09-16"))

    price_rows = []
    for (card_id, price_date), price in prices.items():
        price_rows.append((card_id, price_date, price))

    print("Rows ready:", len(set_rows), "sets |", len(cards), "cards |", len(price_rows), "prices")

    # 3. Load into Neon
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))

    with conn:
        with conn.cursor() as cur:
            execute_values(cur, """
                INSERT INTO sets (set_id, set_name, release_date) VALUES %s
                ON CONFLICT (set_id) DO NOTHING
            """, set_rows)

            execute_values(cur, """
                INSERT INTO cards (card_id, set_id, card_name, card_number,
                                   rarity, printing, tcgplayer_id) VALUES %s
                ON CONFLICT (card_id) DO NOTHING
            """, cards)

            execute_values(cur, """
                INSERT INTO price_history (card_id, price_date, price_usd) VALUES %s
                ON CONFLICT (card_id, price_date)
                DO UPDATE SET price_usd = EXCLUDED.price_usd, loaded_at = NOW()
            """, price_rows)

    conn.close()
    print("Load complete.")


if __name__ == "__main__":
    load()