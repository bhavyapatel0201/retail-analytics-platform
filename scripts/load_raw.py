"""
Load the nine Olist CSVs into a local DuckDB file under the `raw` schema.

Usage (from the repo root):
    python scripts/load_raw.py

Raw tables are loaded exactly as they arrive, with every column as text.
No cleaning happens here: every transformation belongs in dbt, where it is
tested and version controlled.
"""
import argparse
import sys
from pathlib import Path

import duckdb

# source file -> raw table name
FILES = {
    "olist_orders_dataset.csv": "orders",
    "olist_order_items_dataset.csv": "order_items",
    "olist_customers_dataset.csv": "customers",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_geolocation_dataset.csv": "geolocation",
    "product_category_name_translation.csv": "product_category_translation",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default="data/retail_dev.duckdb", help="DuckDB file to load into")
    parser.add_argument("--raw-dir", default="data/raw", help="Folder containing the source CSVs")
    args = parser.parse_args()

    raw_dir = Path(args.raw_dir)
    missing = [f for f in FILES if not (raw_dir / f).exists()]
    if missing:
        print(f"Missing files in {raw_dir}/:")
        for name in missing:
            print(f"  - {name}")
        return 1

    Path(args.db).parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(args.db)
    con.execute("CREATE SCHEMA IF NOT EXISTS raw")

    for filename, table in FILES.items():
        path = (raw_dir / filename).as_posix()
        # all_varchar keeps the landing layer untyped; dbt staging does the casting.
        con.execute(
            f"""
            CREATE OR REPLACE TABLE raw.{table} AS
            SELECT * FROM read_csv('{path}', header = true, all_varchar = true)
            """
        )
        n = con.execute(f"SELECT count(*) FROM raw.{table}").fetchone()[0]
        print(f"  raw.{table:<30} {n:>10,} rows")

    con.close()
    print(f"\nLoaded into {args.db}")
    return 0


if __name__ == "__main__":
    sys.exit(main())