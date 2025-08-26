-- Test to check for amount discrepancies between calculated and original totals
-- Returns orders where calculated_total differs from original_total

SELECT 
    order_id,
    original_total,
    calculated_total,
    ABS(calculated_total - original_total) as difference,
    'Amount discrepancy detected' as issue
FROM {{ ref('fct_orders') }}
WHERE 1 = 1
    AND ABS(calculated_total - original_total) > 0.01
