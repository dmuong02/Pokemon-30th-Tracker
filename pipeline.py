from fetch_prices import fetch
from load_prices import load

print("=== Step 1: Extract ===")
fetch()

print("\n=== Step 2: Transform + Load ===")
load()

print("\nPipeline finished.")