-- Simple Consistency Test
-- Checks if the total number of orders is correct

-- Verifies if the number of orders in dim_customers matches stg_orders
SELECT 
    c.customer_id,
    c.total_orders as expected_orders,
    COUNT(o.order_id) as actual_orders,
    'Order count mismatch' as issue
FROM {{ ref('dim_customers') }} c
LEFT JOIN {{ ref('stg_orders') }} o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.total_orders
HAVING c.total_orders != COUNT(o.order_id)
