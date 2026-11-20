-- The source has many lat/lng rows per zip prefix. Collapse to one row per
-- prefix: average coordinates, most common city and state.
with typed as (
    select
        lpad(geolocation_zip_code_prefix, 5, '0') as zip_code_prefix,
        cast(geolocation_lat as double)           as lat,
        cast(geolocation_lng as double)           as lng,
        lower(trim(geolocation_city))             as city,
        upper(trim(geolocation_state))            as state
    from {{ source('olist', 'geolocation') }}
)
select
    zip_code_prefix,
    avg(lat)    as lat,
    avg(lng)    as lng,
    mode(city)  as city,
    mode(state) as state
from typed
group by zip_code_prefix