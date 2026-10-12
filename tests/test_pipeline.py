import json
import sqlite3

from src.pipeline.main import run


def test_end_to_end(tmp_path):
    raw = [
        {"id": 1, "sku": "a-1", "title": "Pen", "category": "stationery",
         "price": 2.5, "stock": 10, "brand": "Bic"},
        {"id": 2, "sku": "a-1", "title": "Pen again", "category": "stationery",
         "price": 2.5, "stock": 10},                                   # duplicate sku
        {"id": 3, "sku": "b-2", "title": "Book", "category": "books",
         "price": None, "stock": 4},                                   # missing price
    ]
    input_file = tmp_path / "raw.json"
    input_file.write_text(json.dumps(raw))
    db = tmp_path / "test.db"
    report = tmp_path / "rejected.csv"

    summary = run(str(input_file), str(db), str(report))

    assert summary == {"total": 3, "loaded": 1, "rejected": 2}
    conn = sqlite3.connect(db)
    assert conn.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 1
    conn.close()
    assert "duplicate sku" in report.read_text()
