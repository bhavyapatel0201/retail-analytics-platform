"""
Profile the raw Olist tables and print the data quality findings.

Run from the repo root:
    python scripts/profile_raw.py

Each section answers one question. The results become the defects table in
the README and the devlog entry for Phase 1.
"""
import duckdb

con = duckdb.connect("data/retail_dev.duckdb", read_only=True)

CHECKS = [
    ("Date range of orders",
     """select min(order_purchase_timestamp) as first_order,
               max(order_purchase_timestamp) as last_order
        from raw.orders"""),

    ("Order statuses",
     """select order_status, count(*) as orders
        from raw.orders group by 1 order by 2 desc"""),

    ("Orders with no delivery date",
     """select count(*) filter (where order_delivered_customer_date is null) as no_delivery_date,
               count(*) filter (where order_status = 'delivered'
                                 and order_delivered_customer_date is null) as delivered_but_no_date
        from raw.orders"""),

    ("Customers: per-order id vs real person",
     """select count(*) as rows,
               count(distinct customer_id) as customer_ids,
               count(distinct customer_unique_id) as unique_people
        from raw.customers"""),

    ("Reviews: is review_id unique?",
     """select count(*) as rows,
               count(distinct review_id) as distinct_review_ids,
               count(distinct order_id) as orders_reviewed
        from raw.order_reviews"""),

    ("Orders with more than one review",
     """select count(*) as orders_with_multiple_reviews from (
            select order_id from raw.order_reviews group by 1 having count(*) > 1)"""),

    ("Orders with split payments",
     """select count(*) as orders_with_multiple_payment_rows from (
            select order_id from raw.order_payments group by 1 having count(*) > 1)"""),

    ("Geolocation: rows vs distinct zip prefixes",
     """select count(*) as rows,
               count(distinct geolocation_zip_code_prefix) as zip_prefixes
        from raw.geolocation"""),

    ("Products: missing or bad values",
     """select count(*) filter (where product_category_name is null) as null_category,
               count(*) filter (where product_weight_g is null) as null_weight,
               count(*) filter (where product_weight_g = '0') as zero_weight
        from raw.products"""),

    ("Categories missing from the translation table",
     """select distinct p.product_category_name
        from raw.products p
        left join raw.product_category_translation t using (product_category_name)
        where p.product_category_name is not null
          and t.product_category_name_english is null"""),

    ("Orders with no items",
     """select count(*) as orders_without_items
        from raw.orders o
        left join (select distinct order_id from raw.order_items) i using (order_id)
        where i.order_id is null"""),
]

for title, sql in CHECKS:
    print(f"\n=== {title} ===")
    con.sql(sql).show()