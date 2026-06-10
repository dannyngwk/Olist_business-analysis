select
    strftime(purchased_at, '%Y-%m') as order_month,
    count(distinct order_id) as orders,
    round(sum(gmv),2) as gmv,
    round(avg(gmv),2) as avg_order_value
from {{ ref('fct_orders') }}
where order_status = 'delivered'
group by 1 order by 1
