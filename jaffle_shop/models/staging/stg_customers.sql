WITH cleaned AS (

    SELECT
        id AS customer_id,
        TRIM(first_name) AS first_name,
        TRIM(last_name) AS last_name,
        CASE 
            WHEN email LIKE '%@%'
                THEN LOWER(TRIM(email))
        END AS email,
        CASE 
            WHEN phone IS NOT NULL
                THEN {{ clean_phone('phone') }}
        END AS phone,
        TRIM(address) AS address,
        TRIM(city) AS city,
        TRIM(state) AS state,
        TRIM(zip_code) AS zip_code,
        COALESCE(email LIKE '%@%', FALSE) AS has_valid_email,
        CASE
            WHEN phone IS NOT NULL
                AND LENGTH({{ clean_phone('phone') }}) >= 10
                THEN TRUE
            ELSE FALSE 
        END AS has_valid_phone,
        created_at,
        updated_at
    FROM {{ ref('raw_customers') }}
)

SELECT *
FROM cleaned
