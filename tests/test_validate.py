from src.pipeline.validate import split_valid_invalid, validate_record


def good(**overrides):
    record = {"sku": "A1", "title": "Thing", "category": "Toys", "brand": "Acme",
              "price": 10.0, "stock": 3, "rating": 4.2, "discount_pct": 5.0}
    record.update(overrides)
    return record


def test_valid_record_has_no_errors():
    assert validate_record(good()) == []


def test_missing_price_and_negative_stock_are_reported():
    errors = validate_record(good(price=None, stock=-1))
    assert "missing or invalid price" in errors
    assert "stock cannot be negative" in errors


def test_rating_out_of_range():
    assert "rating must be between 0 and 5" in validate_record(good(rating=9.5))


def test_duplicate_sku_is_rejected_but_first_is_kept():
    valid, rejected = split_valid_invalid([good(), good(title="Copy")])
    assert len(valid) == 1
    assert len(rejected) == 1
    assert "duplicate sku" in rejected[0]["reason"]
