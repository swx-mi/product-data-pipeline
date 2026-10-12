"""Extract step: download or read raw product JSON."""
import json
import urllib.request
from pathlib import Path

DUMMYJSON_URL = "https://dummyjson.com/products?limit=0"


def download_products(out_path: str, url: str = DUMMYJSON_URL) -> int:
    """Download the public DummyJSON product catalogue and save it to disk.

    Returns the number of products downloaded.
    """
    with urllib.request.urlopen(url, timeout=30) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    products = payload.get("products", [])
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2)
    return len(products)


def load_products(path: str) -> list[dict]:
    """Read a JSON file containing a list of raw product dicts."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "products" in data:
        data = data["products"]
    if not isinstance(data, list):
        raise ValueError("Expected a JSON list of products")
    return data
