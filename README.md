# Product Data Pipeline with SQL Validation

A small ETL pipeline that turns raw, nested product JSON into a clean, validated, relational SQL database - and tells you exactly which records were rejected and why.

Built with **Python, SQLite (SQL) and pytest**. Uses only the Python standard library at runtime.

## Why I built it
In my day job I standardise large volumes of messy brand product data into clean product masters for an ERP. This project recreates that workflow on **public sample data** so it can be shared and reviewed.

## Pipeline flow

```
 raw JSON  ->  EXTRACT  ->  TRANSFORM  ->  VALIDATE  ->  LOAD (SQLite)
                                              |
                                              +-> reports/rejected_rows.csv (with reasons)
```

| Step | File | What it does |
|------|------|--------------|
| Extract | `src/pipeline/extract.py` | Downloads/reads product JSON |
| Transform | `src/pipeline/transform.py` | Flattens nested fields, trims text, parses prices like `"$1,299.50"`, standardises SKU and category |
| Validate | `src/pipeline/validate.py` | Required fields, price > 0, stock >= 0, rating 0-5, duplicate SKU detection |
| Load | `src/pipeline/load.py` | Creates normalised tables (`products`, `brands`, `categories`) and writes the rejection report |

## Setup & run

```bash
git clone <your-repo-url>
cd product-data-pipeline
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 1. download public sample data (DummyJSON) and run the pipeline
python -m src.pipeline.main --download

# 2. or create a deliberately messy copy and run on that
python generate_messy_data.py data/raw_products.json data/messy_products.json
python -m src.pipeline.main --input data/messy_products.json
```

Example output:
```
---- Pipeline summary ----
Total rows   : <n>
Loaded       : <n>
Rejected     : <n>  (see reports/rejected_rows.csv)
```

## Explore the data with SQL
```bash
sqlite3 products.db < sql/queries.sql
```
`sql/queries.sql` contains 7 queries: products per category, average price per brand (JOIN + GROUP BY), duplicate detection (HAVING), low stock, data-quality checks, top product per category (correlated subquery) and categories below average rating (subquery in HAVING).

## Database schema
- `categories(id, name UNIQUE)`
- `brands(id, name UNIQUE)`
- `products(id, sku UNIQUE, title, brand_id FK, category_id FK, price CHECK > 0, discount_pct, stock CHECK >= 0, rating CHECK 0..5, weight)`

## Tests
```bash
pytest -q
```

## Possible improvements
- Use `pandas` for very large files; switch SQLite to PostgreSQL
- Add a reconciliation report (source count = loaded + rejected)
- Schedule runs with cron / GitHub Actions

## Data source
Public sample data from [DummyJSON](https://dummyjson.com/products). No company data is used.
