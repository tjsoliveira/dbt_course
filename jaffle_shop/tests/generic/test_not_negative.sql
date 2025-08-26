-- Generic test to check for non-negative values
-- Returns rows where the column has negative values (only for non-null values)
{% test not_negative(model, column_name) %}

SELECT {{ column_name }}
FROM {{ model }}
WHERE {{ column_name }} IS NOT NULL
  AND {{ column_name }} < 0

{% endtest %}