-- Generic test to check for valid dates
-- Returns rows where the column is not a valid date

{% test valid_date(model, column_name) %}

SELECT {{ column_name }}
FROM {{ model }}
WHERE {{ column_name }} IS NOT NULL
  AND (
    {{ column_name }} = ''
    OR {{ column_name }} = '0000-00-00'
    OR {{ column_name }} = '1900-01-01'
    OR {{ column_name }} = '9999-12-31'
    OR {{ column_name }} < '1900-01-01'
    OR {{ column_name }} > '2100-12-31'
  )

{% endtest %}