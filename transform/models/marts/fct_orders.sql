-- One row per order: revenue, delivery performance, satisfaction
with o as (select * from {{ ref('stg_orders') }}),
items as (
    select order_id, sum(price) as items_revenue, sum(freight_value) as freight,
           count(*) as item_count
    from {{ ref('stg_order_items') }} group by 1),
pay as (
    select order_id, sum(payment_value) as payment_value, max(installments) as max_installments
    from {{ ref('stg_order_payments') }} group by 1),
rev as (select order_id, avg(review_score) as review_score from {{ ref('stg_order_reviews') }} group by 1),
cust as (select * from {{ ref('stg_customers') }})
select
    o.order_id, o.order_status,
    c.customer_unique_id, c.state as customer_state, c.city as customer_city,
    o.purchased_at, o.delivered_at, o.estimated_delivery_at,
    date_diff('day', o.purchased_at, o.delivered_at) as delivery_days,
    case when o.delivered_at > o.estimated_delivery_at then true else false end as is_late,
    coalesce(i.items_revenue,0) as items_revenue,
    coalesce(i.freight,0)       as freight,
    coalesce(i.items_revenue,0)+coalesce(i.freight,0) as gmv,
    i.item_count, p.payment_value, p.max_installments, r.review_score
from o
left join items i using (order_id)
left join pay p using (order_id)
left join rev r using (order_id)
left join cust c on o.customer_id = c.customer_id
