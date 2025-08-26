WITH cleaned AS (

    SELECT
        -- Primary key
        id AS product_id,
        
        -- Product identification
        TRIM(sku) AS sku,
        TRIM(name) AS product_name,
        
        -- Categorization
        TRIM(category) AS category,
        TRIM(subcategory) AS subcategory,
        TRIM(brand) AS brand,
        
        -- Pricing and validation
        CASE 
            WHEN price >= 0 THEN price
            ELSE 0 
        END AS price,
        
        -- Description cleaning
        CASE 
            WHEN description IS NOT NULL
                AND LENGTH(TRIM(description)) > 0
                THEN TRIM(description)
            ELSE 'Descrição não disponível'
        END AS description,
        
        -- Timestamps
        created_at,
        
        -- Business logic flags
        COALESCE(price > 100, FALSE) AS is_premium_product,
        COALESCE(price > 500, FALSE) AS is_luxury_product,
        COALESCE(price < 50, FALSE) AS is_budget_product,
        
        -- Category-specific flags
        COALESCE(category = 'Electronics', FALSE) AS is_electronics,
        COALESCE(category IN ('Clothing', 'Beauty'), FALSE) AS is_fashion,
        COALESCE(category IN ('Sports', 'Health'), FALSE) AS is_sports_health,
        
        -- Brand tier classification
        CASE 
            WHEN brand IN ('Apple', 'Samsung', 'Sony', 'LG', 'Dell', 'HP', 'Canon', 'Nikon')
                THEN 'Premium'
            WHEN brand IN ('Nike', 'Adidas', 'Under Armour', 'Puma')
                THEN 'Sports Premium'
            WHEN brand IN ('Zara', 'H&M', 'Calvin Klein')
                THEN 'Fashion Premium'
            WHEN brand IN ('Natura', 'Avon', 'O Boticário')
                THEN 'Beauty Premium'
            WHEN brand IN ('Tramontina', 'Tigre', 'Brastemp', 'Electrolux')
                THEN 'Home Premium'
            ELSE 'Standard'
        END AS brand_tier,
        
        -- Price range classification
        CASE 
            WHEN price < 25
                THEN 'Budget'
            WHEN price BETWEEN 25 AND 100
                THEN 'Standard'
            WHEN price BETWEEN 100 AND 500
                THEN 'Premium'
            WHEN price > 500
                THEN 'Luxury'
            ELSE 'Unknown'
        END AS price_range
    FROM {{ ref('raw_products') }}
)

SELECT * 
FROM cleaned
