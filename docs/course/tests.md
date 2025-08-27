# 🧪 Tests in dbt

## 🎯 What are Tests?

Tests in dbt are **SQL queries that return failing rows**. They're your data quality guardians that ensure your transformations produce reliable, accurate data. In dbt, tests are:

- **Assertions** about your data that should always be true
- **Quality gates** that prevent bad data from reaching production
- **Documentation** that describes expected data behavior
- **Automated checks** that run with every dbt execution

## 🔍 How Tests Work

When you run `dbt test`, dbt:

1. **Compiles** your test SQL into executable queries
2. **Executes** each test against your data warehouse
3. **Evaluates** results - if any rows are returned, the test fails
4. **Reports** which tests passed or failed
5. **Stops execution** (optionally) if critical tests fail

## 📝 Test Anatomy

A basic test follows this pattern:

```sql
-- This test PASSES if it returns zero rows
-- This test FAILS if it returns any rows

SELECT *
FROM {{ ref('my_model') }}
WHERE condition_that_should_never_be_true
```

## 🏗️ Types of Tests in dbt

### **1. Built-in Tests** ⚡

dbt comes with four essential tests out of the box:

```yaml
# schema.yml
models:
  - name: stg_customers
    columns:
      - name: customer_id
        data_tests:
          - unique          # No duplicate values
          - not_null        # No missing values
      - name: status
        data_tests:
          - accepted_values:
              values: ['active', 'inactive']
      - name: created_date
        data_tests:
          - relationships:
              to: ref('dim_date')
              field: date_key
```

### **2. dbt_utils Tests** 🛠️

The `dbt_utils` package provides powerful additional tests:

#### **Expression Tests**
```yaml
# From our Jaffle Shop project
- name: total_amount
  data_tests:
    - dbt_utils.expression_is_true:
        arguments:
          expression: ">= 0"

- name: quantity  
  data_tests:
    - dbt_utils.expression_is_true:
        arguments:
          expression: "> 0"
```

#### **Other dbt_utils Tests**
- `dbt_utils.unique_combination_of_columns` - Multi-column uniqueness
- `dbt_utils.not_null_proportion` - Percentage of non-null values
- `dbt_utils.recency` - Data freshness checks
- `dbt_utils.equal_rowcount` - Compare row counts between tables

### **3. Custom Generic Tests** 🎨

Create reusable tests for your specific business logic:

#### **`test_empty_string.sql`**
```sql
{% test empty_string(model, column_name) %}

SELECT {{ column_name }}
FROM {{ model }}
WHERE LENGTH(TRIM({{ column_name }})) = 0

{% endtest %}
```

#### **`test_not_negative.sql`** 
```sql
{% test not_negative(model, column_name) %}

SELECT {{ column_name }}
FROM {{ model }}
WHERE {{ column_name }} IS NOT NULL
  AND {{ column_name }} < 0

{% endtest %}
```

#### **`test_valid_date.sql`**
```sql
{% test valid_date(model, column_name) %}

SELECT {{ column_name }}
FROM {{ model }}
WHERE {{ column_name }} IS NOT NULL 
  AND (
    {{ column_name }} < '1900-01-01'
    OR {{ column_name }} > CURRENT_DATE + INTERVAL '1 year'
  )

{% endtest %}
```

### **4. Singular Tests** 🎯

Business-specific tests that don't fit the generic pattern:

#### **`test_consistency.sql`**
```sql
-- Verifies if the number of orders in dim_customers matches stg_orders
SELECT 
    c.customer_id,
    c.total_orders as expected_orders,
    COUNT(o.order_id) as actual_orders,
    'Order count mismatch' as issue
FROM {{ ref('dim_customers') }} c
LEFT JOIN {{ ref('stg_orders') }} o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.total_orders
HAVING c.total_orders != COUNT(o.order_id)
```

#### **`test_daily_sales_consistency.sql`**
```sql
-- Complex validation comparing daily sales summary with order data
WITH daily_order_summary AS (
    SELECT
        DATE(order_date) AS sale_date,
        COUNT(DISTINCT order_id) AS actual_orders,
        SUM(total_amount) AS actual_revenue
    FROM {{ ref('stg_orders') }}
    WHERE order_date IS NOT NULL
    GROUP BY DATE(order_date)
)

SELECT *
FROM {{ ref('daily_sales_summary') }} dss
LEFT JOIN daily_order_summary dos ON dss.sale_date = dos.sale_date
WHERE ABS(dss.total_revenue - dos.actual_revenue) > 0.01
```

## 📊 Real Examples from Jaffle Shop

### **Schema Test Configuration**

```yaml
# models/staging/staging.yml
models:
  - name: stg_customers
    columns:
      - name: customer_id
        data_tests:
          - unique
          - not_null
      
      - name: first_name
        data_tests:
          - not_null:
              config:
                severity: warn
          - empty_string:
              config:
                severity: warn

  - name: stg_orders
    columns:
      - name: total_amount
        data_tests:
          - not_null
          - dbt_utils.expression_is_true:
              arguments:
                expression: ">= 0"
      
      - name: status
        data_tests:
          - accepted_values:
              values: ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
```

### **Test Severity Levels**

```yaml
data_tests:
  - unique:
      config:
        severity: error    # Stops execution (default)
  - not_null:
      config:
        severity: warn     # Continues but reports warning
```

## 🎛️ Test Configuration

### **Test Selection and Execution**

```bash
# Run all tests
dbt test

# Run tests for specific model
dbt test --select stg_customers

# Run only generic tests
dbt test --select test_type:generic

# Run only singular tests  
dbt test --select test_type:singular

# Run tests with warnings
dbt test --store-failures
```

### **Test Documentation**

```yaml
data_tests:
  - unique:
      config:
        severity: error
        error_if: ">= 1"
        warn_if: ">= 1"
        store_failures: true
```

## 💡 Testing Best Practices

### **1. Test Pyramid Strategy**
- **Many** built-in tests (unique, not_null)
- **Some** generic tests (business rules)
- **Few** singular tests (complex scenarios)

### **2. Test Early and Often**
- Test in staging layer for data quality
- Test in analytics layer for business logic
- Test in marts layer for final validation

### **3. Meaningful Test Names**
```sql
-- Good: Describes what the test validates
test_order_amounts_are_positive.sql

-- Bad: Generic or unclear
test_orders.sql
```

### **4. Performance Considerations**
- Use `limit` for large datasets during development
- Consider test execution time in CI/CD pipelines
- Use `store_failures` strategically

### **5. Test Documentation**
```yaml
data_tests:
  - unique:
      name: customer_id_uniqueness
      description: "Ensures each customer appears only once"
```

## 🛠️ Working with Tests

### **Development Workflow**
```bash
# Run model and its tests
dbt run --select stg_customers
dbt test --select stg_customers

# Build model (run + test)
dbt build -s "stg_customers"

# Debug failing tests
dbt test --select stg_customers --store-failures

# Check stored failures
SELECT * FROM my_schema.dbt_test_failures
```

### **CI/CD Integration**
```bash
# Typical CI pipeline
dbt run --select state:modified+
dbt test --select state:modified+

# Or
dbt build -s "state:modified+"
```

## 🎯 Key Takeaways

1. **Tests are SQL queries** that return failing rows
2. **Four built-in tests** cover most basic scenarios
3. **dbt_utils tests** provide advanced functionality
4. **Generic tests** enable custom reusable logic
5. **Singular tests** handle complex business scenarios
6. **Test configuration** controls severity and behavior
7. **Testing strategy** should follow the test pyramid
8. **Documentation and naming** make tests maintainable

---

**Next**: Learn about Documentation to make your dbt project self-documenting!
