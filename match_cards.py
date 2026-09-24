import os
import json
from collections import Counter

import psycopg2
from dotenv import load_dotenv

load_dotenv()

with open("data/raw/tcgdex_cards.json") as f:
    tcgdex_cards = json.load(f)

# Manual matches for names that differ between sources
manual_map = {
    "Poke Pad": "30th-126",
    "Nidoran F": "30th-087",
    "Gengar (Prime)": "30th-c-018",
    "Darkrai & Cresselia Legend (Top)": "30th-c-019",
    "Darkrai & Cresselia Legend (Bottom)": "30th-c-020",
    "Metagross (Delta Species)": "30th-c-003",
    "Palkia LV.X": "30th-c-022",
    "Genesect EX (Team Plasma)": "30th-c-004",
}

by_id = {t["tcgdex_id"]: t for t in tcgdex_cards}

main_by_number = {}
classic_by_name = {}
for t in tcgdex_cards:
    if t["set_id"] == "30th":
        main_by_number[int(t["local_id"])] = t
    else:
        classic_by_name[t["name"]] = t

main_name_counts = Counter(t["name"] for t in tcgdex_cards if t["set_id"] == "30th")
main_by_name = {}
for t in tcgdex_cards:
    if t["set_id"] == "30th" and main_name_counts[t["name"]] == 1:
        main_by_name[t["name"]] = t

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
with conn.cursor() as cur:
    cur.execute("SELECT card_id, set_id, card_name, card_number FROM cards")
    db_cards = cur.fetchall()
conn.close()

matched = []
unmatched = []
name_mismatches = []

for card_id, set_id, card_name, card_number in db_cards:
    t = None
    if card_name in manual_map:
        label = "manual"
        t = by_id[manual_map[card_name]]
    elif set_id == "me-30th-celebration-pokemon":
        label = "main"
        number = card_number.split("/")[0] if card_number else ""
        if number.isdigit():
            t = main_by_number.get(int(number))
        else:
            t = main_by_name.get(card_name)
    else:
        label = "classic"
        t = classic_by_name.get(card_name)

    if t is None:
        unmatched.append(card_name + " [" + label + "]")
    else:
        matched.append((card_id, t))
        if t["name"] != card_name:
            name_mismatches.append((card_name, t["name"]))

print("Matched:", len(matched), "of", len(db_cards))

print("\nUnmatched (JustTCG side):")
for name in unmatched:
    print("  -", name)

print("\nMatched, but names differ (check these):")
for ours, theirs in name_mismatches:
    print("  -", ours, "vs", theirs)

used_ids = {t["tcgdex_id"] for _, t in matched}
print("\nLeftover (TCGdex side):")
for t in tcgdex_cards:
    if t["tcgdex_id"] not in used_ids:
        print("  -", t["tcgdex_id"], "|", t["name"])

# Write to the database only if every card matched
if unmatched:
    print("\nNot writing to the database until every card matches.")
else:
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    with conn:
        with conn.cursor() as cur:
            for card_id, t in matched:
                cur.execute(
                    "UPDATE cards SET illustrator = %s, card_number = %s WHERE card_id = %s",
                    (t["illustrator"], t["local_id"], card_id),
                )
    conn.close()
    print("\nUpdated", len(matched), "cards with illustrator and card number.")