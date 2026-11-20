select
    product_id,
    product_category_name                          as category_name_pt,
    cast(product_name_lenght        as integer)    as name_length,          -- misspelled in source
    cast(product_description_lenght as integer)    as description_length,   -- misspelled in source
    cast(product_photos_qty         as integer)    as photos_qty,
    -- zero weight is a data defect, not a real weight: treat as unknown
    nullif(cast(product_weight_g as integer), 0)   as weight_g,
    cast(product_length_cm as integer)             as length_cm,
    cast(product_height_cm as integer)             as height_cm,
    cast(product_width_cm  as integer)             as width_cm
from {{ source('olist', 'products') }}