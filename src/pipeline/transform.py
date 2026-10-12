"""Transform step: flatten nested JSON and standardise values."""
import re
from typing import Any, Optional

DEFAULT_BRAND = "Unbranded"


def to_float(value: Any) -> Optional[float]:
    """Convert values like 12.5, '12.5', '$1,299.50' to float. None if impossible."""
    if value is None:
        return None
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    if isinstance(value, str):
        cleaned = re.sub(r"[^0-9.\-]", "", value)
        if cleaned in ("", "-", ".", "-."):
            return None
        try:
            return float(cleaned)
        except ValueError:
            return None
    return None


def to_int(value: Any) -> Optional[int]:
    number = to_float(value)
    if number is None:
        return None
    return int(number)


def clean_text(value: Any) -> Optional[str]:
    """Trim and collapse whitespace. Empty strings become None."""
    if value is None:
        return None
    text = re.sub(r"\s+", " ", str(value)).strip()
    return text or None


def standardise_category(value: Any) -> Optional[str]:
    """'mens-shirts' / ' Mens Shirts ' -> 'Mens Shirts'."""
    text = clean_text(value)
    if text is None:
        return None
    return text.replace("-", " ").replace("_", " ").title()


def standardise_sku(value: Any) -> Optional[str]:
    text = clean_text(value)
    return text.upper() if text else None


def flatten_product(raw: dict) -> dict:
    """Turn one raw (possibly nested) product dict into a flat standard record."""
    dims = raw.get("dimensions") or {}
    return {
        "source_id": raw.get("id"),
        "sku": standardise_sku(raw.get("sku")),
        "title": clean_text(raw.get("title")),
        "brand": clean_text(raw.get("brand")) or DEFAULT_BRAND,
        "category": standardise_category(raw.get("category")),
        "price": to_float(raw.get("price")),
        "discount_pct": to_float(raw.get("discountPercentage")),
        "stock": to_int(raw.get("stock")),
        "rating": to_float(raw.get("rating")),
        "weight": to_float(raw.get("weight")),
        "width": to_float(dims.get("width")),
        "height": to_float(dims.get("height")),
        "depth": to_float(dims.get("depth")),
    }


def transform_all(raw_products: list[dict]) -> list[dict]:
    return [flatten_product(p) for p in raw_products]
