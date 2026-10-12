"""Load step: write clean records into SQLite and rejected rows into a CSV report."""
import csv
import sqlite3
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "sql" / "schema.sql"

REJECT_COLUMNS = ["source_id", "sku", "title", "brand", "category", "price",
                  "stock", "rating", "reason"]


def init_db(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    return conn


def _get_or_create(conn: sqlite3.Connection, table: str, name: str) -> int:
    conn.execute(f"INSERT OR IGNORE INTO {table} (name) VALUES (?)", (name,))
    row = conn.execute(f"SELECT id FROM {table} WHERE name = ?", (name,)).fetchone()
    return row[0]


def load_products(conn: sqlite3.Connection, records: list[dict]) -> int:
    """Insert valid records. Returns the number of rows inserted."""
    inserted = 0
    for r in records:
        category_id = _get_or_create(conn, "categories", r["category"])
        brand_id = _get_or_create(conn, "brands", r["brand"])
        cur = conn.execute(
            """INSERT OR IGNORE INTO products
               (sku, title, brand_id, category_id, price, discount_pct,
                stock, rating, weight)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (r["sku"], r["title"], brand_id, category_id, r["price"],
             r["discount_pct"], r["stock"], r["rating"], r["weight"]),
        )
        inserted += cur.rowcount
    conn.commit()
    return inserted


def write_rejection_report(rejected: list[dict], report_path: str) -> None:
    Path(report_path).parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=REJECT_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rejected)
