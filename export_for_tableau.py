import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

views = ["v_card_prices", "v_card_summary"]

os.makedirs("data/tableau", exist_ok=True)

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
with conn.cursor() as cur:
    for view in views:
        path = "data/tableau/" + view + ".csv"
        with open(path, "w") as f:
            cur.copy_expert("COPY (SELECT * FROM " + view + ") TO STDOUT WITH CSV HEADER", f)
        print("Exported", view, "to", path)
conn.close()