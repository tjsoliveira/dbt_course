WITH cleaned AS (

    SELECT
        id AS order_id,
        customer_id,
        -- Parse and validate order date
        CASE 
            WHEN order_date IS NOT NULL
                THEN order_date
        END AS order_date,
        -- Standardize status
        LOWER(TRIM(status)) AS status,
        -- Validate and clean amounts
        CASE 
            WHEN total_amount >= 0
                THEN total_amount
            ELSE 0 
        END AS total_amount,
        -- Standardize payment method
        LOWER(TRIM(payment_method)) AS payment_method,
        -- Clean delivery address
        TRIM(delivery_address) AS delivery_address,
        -- Add business logic flags
        COALESCE(total_amount > 1000, FALSE) AS is_high_value_order,
        COALESCE(status IN ('delivered', 'shipped'), FALSE) AS is_fulfilled,
        -- Timestamps
        created_at
    FROM {{ ref('raw_orders') }}

)

SELECT *
FROM cleaned
