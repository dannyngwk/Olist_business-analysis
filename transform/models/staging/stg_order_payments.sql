with src as (select * from {{ source('raw','order_payments') }})
select
    order_id,
    cast(payment_sequential as integer)  as payment_sequential,
    lower(payment_type)                  as payment_type,
    cast(payment_installments as integer) as installments,
    cast(payment_value as double)        as payment_value
from src
