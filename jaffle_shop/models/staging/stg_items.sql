WITH source AS (
    SELECT * FROM {{ ref('raw_items') }}
),

cleaned AS (
    SELECT
        item_id,
        order_id,
        product_id,
        -- Validate quantities
        CASE 
            WHEN quantity > 0
                THEN quantity
            ELSE 1 
        END AS quantity,
        -- Validate prices
        CASE 
            WHEN unit_price >= 0
                THEN unit_price
            ELSE 0 
        END AS unit_price,
        -- Calculate total price
        CASE 
            WHEN quantity > 0 AND unit_price >= 0
                THEN quantity * unit_price
            ELSE 0
        END AS calculated_total_price,
        -- Add data quality flags
        COALESCE(quantity > 10, FALSE) AS is_bulk_order,
        COALESCE(unit_price > 50, FALSE) AS is_premium_item,
        -- Timestamps
        created_at
    FROM source
)

SELECT * 
FROM cleaned
