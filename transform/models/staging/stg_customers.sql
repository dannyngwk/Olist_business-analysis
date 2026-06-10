with src as (select * from {{ source('raw','customers') }})
select
    customer_id, customer_unique_id,
    cast(customer_zip_code_prefix as varchar) as zip_code_prefix,
    customer_city as city, upper(customer_state) as state
from src
