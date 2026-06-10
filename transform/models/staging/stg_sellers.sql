select seller_id,
       cast(seller_zip_code_prefix as varchar) as zip_code_prefix,
       seller_city as city, upper(seller_state) as state
from {{ source('raw','sellers') }}
