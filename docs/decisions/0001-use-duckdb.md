# 0001: Use DuckDB as the warehouse

## Status
Accepted

## Context
The project needs a SQL warehouse to run dbt models against. It should cost nothing, require no account setup, and not expire.

## Decision
Use DuckDB through the dbt-duckdb adapter. The warehouse is a single local file.

## Alternatives considered
- **Snowflake:** the 30-day trial expires before the project would be finished and maintained.
- **BigQuery sandbox:** free, but tables expire and it needs a cloud account.
- **PostgreSQL:** free, but needs a running server and adds setup unrelated to the goal.

## Consequences
- Zero cost and a fully reproducible setup for anyone cloning the repo.
- Power BI has no native DuckDB connector, so marts are exported to Parquet for the dashboard.
- SQL is kept portable so the project can target Snowflake or BigQuery later by changing the profile.