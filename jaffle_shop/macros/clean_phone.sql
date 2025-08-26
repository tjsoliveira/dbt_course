{% macro clean_phone(phone_column) %}
    {% if target.type == 'sqlite' %}
        -- For SQLite, use nested REPLACE
        REPLACE(
            REPLACE(
                REPLACE(
                    REPLACE(
                        REPLACE(
                            REPLACE({{ phone_column }}, '-', ''),
                            '(', ''),
                            ')', ''),
                        ' ', ''),
                    '.', ''),
                '+', '')
    {% else %}
        -- For other databases (PostgreSQL, BigQuery, etc), use REGEXP_REPLACE
        REGEXP_REPLACE({{ phone_column }}, '[^0-9]', '', 'g')
    {% endif %}
{% endmacro %}
