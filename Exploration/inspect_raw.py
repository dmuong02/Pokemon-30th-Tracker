import json
from collections import Counter

with open("data/raw/justtcg_2026-09-22.json") as f:
    cards = json.load(f)

print("Total items:", len(cards))

no_prices = []
for c in cards:
    if len(c["variants"]) == 0:
        no_prices.append(c["name"])

print("\nItems with no NM prices:", len(no_prices))
for name in no_prices:
    print("  -", name)

rarities = Counter(c.get("rarity") for c in cards)
print("\nRarity counts:")
for rarity, count in rarities.most_common():
    print(" ", rarity, ":", count)

variant_counts = Counter(len(c["variants"]) for c in cards)
print("\nVariants per card:", dict(variant_counts))

total_points = 0
for c in cards:
    for v in c["variants"]:
        total_points = total_points + len(v.get("priceHistory") or [])

print("\nTotal history points:", total_points)