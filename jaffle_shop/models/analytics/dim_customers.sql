WITH customer_metrics AS (

    SELECT
        c.customer_id,
        c.first_name,
        c.last_name,
        c.email,
        c.city,
        c.state,
        c.has_valid_email,
        c.has_valid_phone,
        -- Order metrics
        COUNT(o.order_id) AS total_orders,
        SUM(CASE
            WHEN o.order_id IS NOT NULL
                THEN 1
            ELSE 0
        END) AS orders_count,
        SUM(o.total_amount) AS total_spent,
        AVG(o.total_amount) AS avg_order_value,
        MAX(o.total_amount) AS max_order_value,
        MIN(o.total_amount) AS min_order_value,
        -- Customer behavior flags
        CASE
            WHEN COUNT(o.order_id) > 5
                THEN TRUE
            ELSE FALSE
        END AS is_frequent_customer,
        CASE
            WHEN SUM(o.total_amount) > 500
                THEN TRUE
            ELSE FALSE
        END AS is_high_value_customer,
        CASE
            WHEN AVG(o.total_amount) > 100
                THEN TRUE
            ELSE FALSE
        END AS is_premium_customer,
        -- First and last order dates
        MIN(o.order_date) AS first_order_date,
        MAX(o.order_date) AS last_order_date,
        -- Customer creation date
        c.created_at
    FROM  {{ ref('stg_customers') }} AS c
    LEFT JOIN {{ ref('stg_orders') }} AS o 
        ON c.customer_id = o.customer_id
    GROUP BY 
        c.customer_id, c.first_name, c.last_name, c.email, c.city, c.state,
        c.has_valid_email, c.has_valid_phone, c.created_at
)

SELECT * 
FROM customer_metrics
