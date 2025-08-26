WITH potential_duplicates AS (

    SELECT
        first_name,
        last_name,
        email,
        phone,
        COUNT(*) AS duplicate_count,
        STRING_AGG(CAST(customer_id AS STRING), ', ') AS customer_ids,
        STRING_AGG(city, ', ') AS cities,
        STRING_AGG(state, ', ') AS states
    FROM {{ ref('stg_customers') }}
    WHERE 1 = 1
        AND (
            (first_name IS NOT NULL AND last_name IS NOT NULL)
            OR (email IS NOT NULL)
            OR (phone IS NOT NULL)
        )
    GROUP BY 
        first_name, last_name, email, phone
    HAVING COUNT(*) > 1

)

SELECT * 
FROM potential_duplicates
