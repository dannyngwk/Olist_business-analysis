with i as (select * from {{ ref('stg_order_items') }}),
p as (select * from {{ ref('stg_products') }}),
r as (select order_id, avg(review_score) review_score from {{ ref('stg_order_reviews') }} group by 1)
select
    p.category,
    count(*) as items_sold,
    count(distinct i.order_id) as orders,
    round(sum(i.price),2) as revenue,
    round(avg(i.price),2) as avg_item_price,
    round(avg(r.review_score),2) as avg_review_score
from i
join p using (product_id)
left join r using (order_id)
where p.category is not null
group by 1
