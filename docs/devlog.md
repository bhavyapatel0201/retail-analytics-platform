# Dev Log

## 2026-11-19
- Created the repo, virtual environment, and installed dbt-core and dbt-duckdb.
- Initialised the dbt project; scaffold merged in PR #1.
- Configured the DuckDB profile, layer materializations, and dbt_utils.
- Issues hit: (write what actually went wrong, e.g. PowerShell vs bash commands, a commit landing on main instead of a branch, requirements pasted into the terminal instead of a file)
- Customers: 99,441 customer_ids vs 96,096 unique people (customer_id is per order; the real key is customer_unique_id).
- Reviews: 98,410 distinct review_ids across 99,224 rows; 547 orders have more than one review; ~768 orders have no review.
- 2,961 orders have split payments (multiple payment rows).
- Deleted a nested folder to clean up a misplaced file and took `_sources.yml` with it. Lesson: list a folder's contents (`Get-ChildItem -Recurse`) before a recursive delete.

## 2026-11-20 - Phase 2: staging layer

- Built nine staging views: rename, cast and trim only, no business logic.
- Geolocation collapsed from 1,000,163 rows to 19,015 (one per zip prefix; average coordinates, most common city and state).
- Zero product weights turned into nulls; misspelled source columns (`product_name_lenght`) renamed.
- `dbt build --select staging`: 9 views and 8 source tests pass (PASS=17).
- Problems hit: deleted `_sources.yml` while cleaning up a nested folder, and `stg_orders.sql` went missing; dbt silently skipped it because the old view still existed in the database. Lesson: compare the model count dbt reports against the files you expect.