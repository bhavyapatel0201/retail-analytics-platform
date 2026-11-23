# retail-analytics-platform

A dbt project that turns the Olist Brazilian e-commerce dataset (nine CSV files, orders from 2016 to 2018) into tested, documented analytics tables. It runs on DuckDB, so it needs no server, account or cost.

## Status

| Layer | State |
|---|---|
| Raw loader | Done: loads the nine CSVs into DuckDB as text, with no cleaning |
| Staging | Done: nine views that rename, cast and trim only (9 views, 8 source tests passing) |
| Intermediate | Not started |
| Marts (core, analytics) | Not started |

Details and decisions are in [`docs/devlog.md`](docs/devlog.md), [`docs/decisions/`](docs/decisions) and [`CHANGELOG.md`](CHANGELOG.md).

## Quick start
python -m venv .venv
.venv\Scripts\activate # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
dbt deps

Put the nine Olist CSVs in `data/raw/`, then:
## Design choices

- **DuckDB as the warehouse:** free, reproducible, one local file. Marts are planned to export to Parquet for a Power BI dashboard (see ADR-0001).
- **All cleaning lives in dbt:** the loader keeps every column as text so each transformation is tested and version controlled.
- **Data findings that shaped the models:** `customer_id` is per order, so the real customer key is `customer_unique_id`; some orders have split payments or several reviews; geolocation collapses from about 1,000,000 rows to one row per zip prefix.

## Layout

License: see [LICENSE](LICENSE).