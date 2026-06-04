with c as (select * from {{ ref('stg_customers') }}),
ord as (select * from {{ ref('stg_orders') }})
select
    c.customer_unique_id,
    max(c.state) as state, max(c.city) as city,
    count(distinct o.order_id) as order_count,
    case when count(distinct o.order_id) > 1 then true else false end as is_repeat
from c left join ord o on c.customer_id = o.customer_id
group by 1
