# Pokémon TCG 30th Celebration Price Tracker

I built this project to track the market prices of every card in Pokémon TCG's 30th Celebration set, which came out on September 16, 2026. A Python script collects prices every day and stores them in a PostgreSQL database, and I use SQL and Tableau to look at how the prices change.

**[View the dashboard on Tableau Public](https://public.tableau.com/views/PokmonTCG30thCelebrationPriceTracker/PriceTracker)**

![Dashboard preview](images/dashboard.png)

## What I Wanted to Find Out

1. How do card prices change in the weeks after a set is released?
2. What makes one card worth more than another: its rarity, the Pokémon, or the artwork?

## What I Found So Far (as of October 12, 2026)

- Prices fell for almost every card after release. The cheapest cards (Commons and Rares) dropped from about $0.90 to about $0.20 the day after release and have stayed there.
- The most valuable new cards kept falling for weeks. Futuristic Rares and Special Illustration Rares started around $190 and $115 and are now both around $50.
- Illustration Rares dropped from about $10 to about $5 in early October, around when the October 2 products (Booster Bundles and Mini Tins) came out. The timing lines up, but I can't prove the new products caused it.
- The three hidden "RGB Mew" cards are by far the most valuable cards in the set, worth thousands of dollars each.
- Artwork still matters, but every Pikachu has lost value. All 30 Pikachu Rares are cheaper than on release day. Shinji Kanda's is still the most valuable at about $2, down from over $6 in late September..

## How It Works

1. **Collect:** `fetch_prices.py` requests prices for all 188 cards from the JustTCG API and saves the results to a JSON file.
2. **Clean and load:** `load_prices.py` cleans the data (for example, separating card names from card numbers) and loads it into three tables in a Neon PostgreSQL database: `sets`, `cards`, and `price_history`.
3. **Automate:** GitHub Actions runs both scripts every morning, so new prices are added without me running anything.
4. **Add artist info:** `fetch_tcgdex.py` and `match_cards.py` pull each card's illustrator from a second API (TCGdex) and match it to the right card in my database.
5. **Analyze:** I wrote SQL views that compare each card's release-day price with its latest price, exported them to CSV, and built the dashboard in Tableau Public.

Two things I made sure of:

- Running the scripts again updates existing rows instead of creating duplicates, because each card can only have one price per day in the database.
- Each run re-downloads the last 30 days of prices, so if a daily run is missed, the next one fills in the gap.

## Choosing a Data Source

I tested three APIs before starting:

- **pokemontcg.io** didn't have prices for recent sets and sometimes returned errors.
- **TCGdex** didn't have prices for this set yet, so I used it for artist names instead.
- **JustTCG** had daily prices going back to release day, so I used it for prices.

## Limitations

- Prices are market averages, not individual sales, and release-day prices are based on only a few sales.
- I assumed all 30 Pikachu cards are equally easy to pull from packs. If some are rarer, that could explain part of the price difference.
- Only 2 cards are Futuristic Rares, so I can't draw strong conclusions about that rarity.
- The raw price data isn't included in this repo because JustTCG's terms don't allow sharing it.
- The three "RGB Mew" secret rares aren't on official card lists. JustTCG began tracking the G/RGB Mew on September 25, so it has no release-day price.
- The three “RGB Mew” secret rares aren’t on official card lists. JustTCG began tracking them between September 25 and October 7, so they have no release-day prices and are excluded from the price-since-release chart.
In early October, JustTCG changed its card IDs, which created duplicate cards in my database. I matched the old and new IDs using TCGplayer product IDs, copied over the illustrator data, and removed the duplicates.

## What I Learned

- Working with APIs: reading documentation, requesting results page by page, and staying under rate limits.
- Designing database tables and writing SQL joins, views, and window functions for analysis.
- Scheduling scripts with GitHub Actions and keeping API keys private with secrets.
- Matching data between two sources that name the same cards differently.
- Choosing chart types in Tableau, like using a log scale when prices range from $0.10 to $300.

## Tools

Python (requests, psycopg2) · PostgreSQL (Neon) · SQL · GitHub Actions · Tableau Public

## Next Steps

- **After November 6:** check whether new product releases lower Classic Collection prices.
- **Mid-December:** update the dashboard and findings with the full release period.
