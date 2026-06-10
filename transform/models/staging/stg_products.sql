with p as (select * from {{ source('raw','products') }}),
     t as (select * from {{ source('raw','category_translation') }})
select
    p.product_id,
    coalesce(t.product_category_name_english, p.product_category_name) as category,
    cast(p.product_weight_g as double)  as weight_g,
    cast(p.product_length_cm as double) as length_cm,
    cast(p.product_height_cm as double) as height_cm,
    cast(p.product_width_cm as double)  as width_cm
from p left join t using (product_category_name)
