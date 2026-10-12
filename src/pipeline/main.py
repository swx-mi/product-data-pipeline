"""Command line entry point.

Usage (from project root):
    python -m src.pipeline.main --download
    python -m src.pipeline.main --input data/messy_products.json
"""
import argparse
import os

from src.pipeline import extract, load, transform, validate


def run(input_path: str, db_path: str, report_path: str) -> dict:
    raw = extract.load_products(input_path)
    flat = transform.transform_all(raw)
    valid, rejected = validate.split_valid_invalid(flat)

    if os.path.exists(db_path):
        os.remove(db_path)  # fresh run each time keeps results reproducible
    conn = load.init_db(db_path)
    inserted = load.load_products(conn, valid)
    conn.close()

    load.write_rejection_report(rejected, report_path)
    return {"total": len(raw), "loaded": inserted, "rejected": len(rejected)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Product data pipeline")
    parser.add_argument("--download", action="store_true",
                        help="download raw products from DummyJSON first")
    parser.add_argument("--input", default="data/raw_products.json")
    parser.add_argument("--db", default="products.db")
    parser.add_argument("--report", default="reports/rejected_rows.csv")
    args = parser.parse_args()

    if args.download:
        count = extract.download_products(args.input)
        print(f"Downloaded {count} products to {args.input}")

    summary = run(args.input, args.db, args.report)
    print("---- Pipeline summary ----")
    print(f"Total rows   : {summary['total']}")
    print(f"Loaded       : {summary['loaded']}")
    print(f"Rejected     : {summary['rejected']}  (see {args.report})")


if __name__ == "__main__":
    main()
