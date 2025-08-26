{{
  config(
    enabled = false
    )
}}

-- Test that daily sales summary is consistent with order data
WITH daily_order_summary AS (
    SELECT
        DATE(order_date) AS sale_date,
        COUNT(DISTINCT order_id) AS actual_orders,
        COUNT(DISTINCT customer_id) AS actual_customers,
        SUM(total_amount) AS actual_revenue
    FROM {{ ref('stg_orders') }}
    WHERE order_date IS NOT NULL
    GROUP BY DATE(order_date)
),

validation AS (
    SELECT
        dss.sale_date,
        dss.total_orders AS expected_orders,
        dos.actual_orders,
        dss.unique_customers AS expected_customers,
        dos.actual_customers,
        dss.total_revenue AS expected_revenue,
        dos.actual_revenue,
        ABS(dss.total_orders - dos.actual_orders) AS order_difference,
        ABS(dss.unique_customers - dos.actual_customers) AS customer_difference,
        ABS(dss.total_revenue - dos.actual_revenue) AS revenue_difference
    FROM {{ ref('daily_sales_summary') }} dss
    LEFT JOIN daily_order_summary dos 
        ON dss.sale_date = dos.sale_date
)

SELECT *
FROM validation
WHERE order_difference > 0 OR customer_difference > 0 OR revenue_difference > 0.01
