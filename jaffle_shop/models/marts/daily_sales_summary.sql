WITH filtered_orders AS (

    SELECT * 
    FROM {{ ref('stg_orders') }}
    WHERE 1 = 1
        AND order_date IS NOT NULL

)

, daily_metrics AS (

    SELECT
        DATE(o.order_date) AS sale_date,
        -- Sales metrics
        COUNT(DISTINCT o.order_id) AS total_orders,
        COUNT(DISTINCT o.customer_id) AS unique_customers,
        SUM(o.total_amount) AS total_revenue,
        AVG(o.total_amount) AS avg_order_value,
        -- Item metrics
        SUM(i.quantity) AS total_items_sold,
        COUNT(DISTINCT i.product_id) AS unique_products_sold,
        -- Payment method distribution
        SUM(
            CASE
                WHEN o.payment_method = 'credit_card'
                    THEN 1
                ELSE 0
            END
        ) AS credit_card_orders,
        SUM(
            CASE
                WHEN o.payment_method = 'debit_card'
                    THEN 1
                ELSE 0
            END
        ) AS debit_card_orders,
        SUM(
            CASE
                WHEN o.payment_method = 'cash'
                    THEN 1
                ELSE 0
            END
        ) AS cash_orders,
        -- Order status distribution
        SUM(
            CASE
                WHEN o.status = 'delivered'
                    THEN 1
                ELSE 0
            END
        ) AS delivered_orders,
        SUM(
            CASE
                WHEN o.status = 'shipped'
                    THEN 1
                ELSE 0
            END
        ) AS shipped_orders,
        SUM(
            CASE
                WHEN o.status = 'pending'
                    THEN 1
                ELSE 0
            END
        ) AS pending_orders,
        SUM(CASE
            WHEN o.status = 'cancelled'
                THEN 1
            ELSE 0
        END) AS cancelled_orders,
        -- High value orders
        SUM(
            CASE
                WHEN o.is_high_value_order
                    THEN 1
                ELSE 0
            END
        ) AS high_value_orders,
        SUM(
            CASE
                WHEN o.is_high_value_order
                    THEN o.total_amount
                ELSE 0
            END
        ) AS high_value_revenue
    FROM filtered_orders AS o
    LEFT JOIN {{ ref('stg_items') }} AS i 
    ON o.order_id = i.order_id
    GROUP BY DATE(o.order_date)

)

SELECT * 
FROM daily_metrics
