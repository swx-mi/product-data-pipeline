from src.pipeline.transform import (
    flatten_product, standardise_category, to_float, to_int, clean_text,
)


def test_to_float_handles_currency_strings():
    assert to_float("$1,299.50") == 1299.50
    assert to_float(12) == 12.0
    assert to_float("abc") is None
    assert to_float(None) is None


def test_to_int_truncates_and_handles_none():
    assert to_int("15") == 15
    assert to_int(None) is None


def test_clean_text_collapses_whitespace():
    assert clean_text("  hello    world ") == "hello world"
    assert clean_text("   ") is None


def test_standardise_category():
    assert standardise_category(" mens-shirts ") == "Mens Shirts"


def test_flatten_product_flattens_dimensions_and_defaults_brand():
    raw = {
        "id": 1, "title": "  Red   Lipstick ", "category": "beauty",
        "price": "9.99", "stock": 5, "sku": "bea-001",
        "dimensions": {"width": 1.5, "height": 2.5, "depth": 3.5},
    }
    flat = flatten_product(raw)
    assert flat["title"] == "Red Lipstick"
    assert flat["sku"] == "BEA-001"
    assert flat["brand"] == "Unbranded"
    assert flat["price"] == 9.99
    assert flat["width"] == 1.5 and flat["depth"] == 3.5
