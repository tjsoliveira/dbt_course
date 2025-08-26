WITH order_summary AS (

    SELECT
        order_id,
        COUNT(*) AS total_items,
        SUM(quantity) AS total_quantity,
        SUM(calculated_total_price) AS calculated_total,
        AVG(unit_price) AS avg_unit_price,
        MAX(unit_price) AS max_unit_price,
        MIN(unit_price) AS min_unit_price
    FROM {{ ref('stg_items') }}
    GROUP BY order_id

)

, final AS (

    SELECT
        o.order_id,
        o.customer_id,
        c.first_name,
        c.last_name,
        c.email,
        c.city,
        c.state,
        o.order_date,
        o.status,
        o.total_amount AS original_total,
        os.calculated_total,
        os.total_items,
        os.total_quantity,
        os.avg_unit_price,
        o.payment_method,
        o.delivery_address,
        o.is_high_value_order,
        o.is_fulfilled,
        c.has_valid_email,
        c.has_valid_phone,
        -- Business logic calculations
        COALESCE(os.calculated_total != o.total_amount, FALSE) AS has_amount_discrepancy,
        CASE 
            WHEN os.calculated_total > o.total_amount
                THEN 'overcharged'
            WHEN os.calculated_total < o.total_amount
                THEN 'undercharged'
            ELSE 'accurate'
        END AS pricing_status,
        -- Customer segmentation
        CASE 
            WHEN o.total_amount > 200
                THEN 'premium'
            WHEN o.total_amount > 100
                THEN 'regular'
            ELSE 'budget'
        END AS customer_segment,
        o.created_at
    FROM {{ ref('stg_orders') }} AS o
    LEFT JOIN {{ ref('stg_customers') }} AS c 
    ON o.customer_id = c.customer_id
    LEFT JOIN order_summary os 
    ON o.order_id = os.order_id

)

SELECT *
FROM final
