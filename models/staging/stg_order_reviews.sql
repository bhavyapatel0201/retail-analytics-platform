-- review_id is NOT unique in the source, so deduplication is an explicit
-- decision made downstream, not hidden in this layer.
select
    review_id,
    order_id,
    cast(review_score as integer)               as review_score,
    review_comment_title                        as comment_title,
    review_comment_message                      as comment_message,
    cast(review_creation_date    as timestamp)  as review_created_at,
    cast(review_answer_timestamp as timestamp)  as review_answered_at
from {{ source('olist', 'order_reviews') }}