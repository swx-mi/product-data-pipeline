"""Create a deliberately messy copy of the raw data so the pipeline has real
problems to catch: duplicates, missing fields, bad prices, negative stock, etc.

Usage:
    python generate_messy_data.py data/raw_products.json data/messy_products.json
"""
import copy
import json
import random
import sys


def make_messy(products: list[dict], seed: int = 42) -> list[dict]:
    rng = random.Random(seed)
    data = copy.deepcopy(products)

    for p in rng.sample(data, k=max(1, len(data) // 10)):      # price as text
        p["price"] = f"${p['price']:,.2f}"
    for p in rng.sample(data, k=max(1, len(data) // 15)):      # negative stock
        p["stock"] = -abs(p.get("stock", 1))
    for p in rng.sample(data, k=max(1, len(data) // 15)):      # missing price
        p["price"] = None
    for p in rng.sample(data, k=max(1, len(data) // 20)):      # missing sku
        p["sku"] = ""
    for p in rng.sample(data, k=max(1, len(data) // 20)):      # impossible rating
        p["rating"] = 9.5
    for p in rng.sample(data, k=max(1, len(data) // 10)):      # messy whitespace / case
        p["title"] = f"   {p['title'].upper()}  "
        p["category"] = f" {p.get('category', '')} "
    data.extend(copy.deepcopy(rng.sample(data, k=max(1, len(data) // 12))))  # duplicates
    rng.shuffle(data)
    return data


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, encoding="utf-8") as f:
        raw = json.load(f)
    messy = make_messy(raw)
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(messy, f, indent=2)
    print(f"Wrote {len(messy)} messy products to {dst}")
