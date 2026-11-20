# Dev Log

## 2026-11-19
- Created the repo, virtual environment, and installed dbt-core and dbt-duckdb.
- Initialised the dbt project; scaffold merged in PR #1.
- Configured the DuckDB profile, layer materializations, and dbt_utils.
- Issues hit: (write what actually went wrong, e.g. PowerShell vs bash commands, a commit landing on main instead of a branch, requirements pasted into the terminal instead of a file)
  - Customers: 99,441 customer_ids vs 96,096 unique people (customer_id is per order; the real key is customer_unique_id).
  - Reviews: 98,410 distinct review_ids across 99,224 rows; 547 orders have more than one review; ~768 orders have no review.
  - 2,961 orders have split payments (multiple payment rows).