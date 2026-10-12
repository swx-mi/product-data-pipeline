"""Validate step: business rules + duplicate detection."""

REQUIRED_FIELDS = ("sku", "title", "category")


def validate_record(record: dict) -> list[str]:
    """Return a list of error messages. An empty list means the record is valid."""
    errors = []

    for field in REQUIRED_FIELDS:
        if not record.get(field):
            errors.append(f"missing {field}")

    price = record.get("price")
    if price is None:
        errors.append("missing or invalid price")
    elif price <= 0:
        errors.append("price must be greater than 0")

    stock = record.get("stock")
    if stock is None:
        errors.append("missing or invalid stock")
    elif stock < 0:
        errors.append("stock cannot be negative")

    rating = record.get("rating")
    if rating is not None and not (0 <= rating <= 5):
        errors.append("rating must be between 0 and 5")

    discount = record.get("discount_pct")
    if discount is not None and not (0 <= discount < 100):
        errors.append("discount_pct must be between 0 and 100")

    return errors


def split_valid_invalid(records: list[dict]) -> tuple[list[dict], list[dict]]:
    """Split records into (valid, rejected). Rejected rows carry a 'reason' field.

    Duplicate SKUs: first occurrence is kept, later ones are rejected.
    """
    valid, rejected = [], []
    seen_skus = set()

    for record in records:
        errors = validate_record(record)
        sku = record.get("sku")
        if sku and sku in seen_skus:
            errors.append("duplicate sku")

        if errors:
            rejected.append({**record, "reason": "; ".join(errors)})
        else:
            valid.append(record)
            seen_skus.add(sku)

    return valid, rejected
