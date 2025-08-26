-- Verify if there are orders with negative or zero values in the total_amount column
SELECT 
    order_id,
    total_amount,
    CASE 
        WHEN total_amount < 0 THEN 'Negative amount'
        WHEN total_amount = 0 THEN 'Zero amount'
        ELSE 'OK'
    END as issue_type
FROM {{ ref('stg_orders') }}
WHERE total_amount <= 0
