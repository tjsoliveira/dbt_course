-- Generic test to check for empty strings
-- Returns rows where the column is empty

{% test empty_string(model, column_name) %}

SELECT {{ column_name }}
FROM {{ model }}
WHERE LENGTH(TRIM({{ column_name }})) = 0

{% endtest %}