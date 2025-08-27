# ⚙️ YAML Configuration in dbt

YAML files are the backbone of dbt documentation and configuration. They define properties for your models, sources, tests, and more. This guide covers everything you need to know about configuring YAML files effectively.

## 📋 YAML File Structure

### Basic Schema Structure

```yaml
version: 2

# Sources configuration
sources:
  - name: source_name
    description: "Description of the source system"
    tables:
      - name: table_name
        description: "Description of the table"

# Models configuration  
models:
  - name: model_name
    description: "Description of the model"
    columns:
      - name: column_name
        description: "Description of the column"

# Seeds configuration
seeds:
  - name: seed_name
    description: "Description of the seed file"

# Snapshots configuration
snapshots:
  - name: snapshot_name
    description: "Description of the snapshot"
```

## 🗂️ Organizing YAML Files

### Option 1: Single schema.yml per Directory
```
models/
├── staging/
│   ├── staging.yml          # All staging models
│   ├── stg_customers.sql
│   └── stg_orders.sql
└── marts/
    ├── marts.yml          # All mart models
    ├── dim_customers.sql
    └── fct_orders.sql
```

### Option 2: Grouped by Subject Area
```
models/
├── staging/
│   ├── _customers__schema.yml    # Customer-related models
│   ├── _orders__schema.yml       # Order-related models
│   ├── stg_customers.sql
│   └── stg_orders.sql
```

### Option 3: One YAML per Model
```
models/
├── staging/
│   ├── stg_customers.yml
│   ├── stg_customers.sql
│   ├── stg_orders.yml
│   └── stg_orders.sql
```

## 📊 Model Configuration

### Complete Model Example

```yaml
version: 2

models:
  - name: stg_customers
    description: |
      Staging table for customer data from the CRM system.
      
      This model cleans and standardizes customer information including:
      - Name standardization
      - Email validation  
      - Phone number formatting
      - Address normalization
      
    meta:
      owner: "data-team@company.com"
      tags: ["pii", "customer", "staging"]
    
    config:
      materialized: table
      post-hook: "GRANT SELECT ON {{ this }} TO read_only_role"
    
    columns:
      - name: customer_id
        description: "Unique identifier for each customer"
        meta:
          dimension:
            type: "primary_key"
        tests:
          - unique
          - not_null
          
      - name: first_name
        description: "Customer's first name, standardized to title case"
        tests:
          - not_null
          
      - name: last_name  
        description: "Customer's last name, standardized to title case"
        tests:
          - not_null
          
      - name: email
        description: |
          Customer's primary email address.
          
        tests:
          - unique
          - not_null
          - accepted_values:
              quote: false
              values: ['contains(@)']
              
      - name: phone
        description: "Formatted phone number in (XXX) XXX-XXXX format"
        
      - name: created_at
        description: "Timestamp when customer record was created"
        tests:
          - not_null
          
      - name: updated_at
        description: "Timestamp when customer record was last updated"
```

## 🔗 Source Configuration

### Complete Source Example

```yaml
version: 2

sources:
  - name: jaffle_shop
    description: |
      Raw data from the Jaffle Shop e-commerce platform.
      
      **Data Refresh**: Updated every hour via Fivetran
      **Owner**: Engineering Team
      **SLA**: 99.9% uptime
      
    meta:
      external_location: "s3://jaffle-shop-data/raw/"
      
    tables:
      - name: customers
        description: |
          Customer master data from the user registration system.
          
          **Source System**: User Management Service
          **Update Frequency**: Real-time via CDC
          **Retention**: 7 years for compliance
          
        columns:
          - name: id
            description: "Primary key - auto-incrementing integer"
            tests:
              - unique
              - not_null
              
          - name: first_name
            description: "Customer first name as entered during registration"
            tests:
              - not_null
              
          - name: last_name
            description: "Customer last name as entered during registration"
            tests:
              - not_null
              
        loaded_at_field: _fivetran_synced
        freshness:
          warn_after: {count: 1, period: hour}
          error_after: {count: 24, period: hour}
          
      - name: orders
        description: "Order transaction data from the e-commerce platform"
        columns:
          - name: id
            description: "Unique order identifier"
            tests:
              - unique
              - not_null
              
          - name: user_id
            description: "Foreign key to customers table"
            tests:
              - not_null
              - relationships:
                  to: source('jaffle_shop', 'customers')
                  field: id
                  
        freshness:
          warn_after: {count: 1, period: hour}
          error_after: {count: 12, period: hour}
```

## 🧪 Test Configuration

### Built-in Tests

```yaml
models:
  - name: stg_customers
    columns:
      - name: customer_id
        tests:
          - unique
          - not_null
          
      - name: status
        tests:
          - accepted_values:
              values: ['active', 'inactive', 'pending']
              
      - name: email
        tests:
          - unique:
              where: "email is not null"
```

### Custom Tests

```yaml
models:
  - name: stg_orders
    tests:
      - assert_positive_order_amount:
          column_name: order_total
      - assert_recent_data:
          column_name: created_at
          interval: 1
          datepart: day
```

## 📝 Documentation Best Practices

### 1. Use Descriptive Names
```yaml
# ❌ Poor
- name: t1
  description: "table"

# ✅ Good  
- name: stg_customers
  description: "Staging table for customer data with cleaned and validated fields"
```

### 2. Include Business Context
```yaml
- name: customer_lifetime_value
  description: |
    Total revenue generated by a customer over their entire relationship.
    
    **Calculation**: Sum of all order amounts minus returns and refunds
    **Business Use**: Customer segmentation and retention analysis
    **Updated**: Daily at 6 AM UTC
```

### 3. Document Data Quality Rules
```yaml
- name: order_amount
  description: |
    Order total amount in USD.
    
    **Valid Range**: $0.01 - $10,000.00
    **Business Rules**: 
    - Cannot be negative
    - Must include tax and shipping
    - Excludes discounts (applied separately)
  tests:
    - not_null
    - dbt_utils.accepted_range:
        min_value: 0.01
        max_value: 10000.00
```

### 4. Use Consistent Formatting
```yaml
# Use consistent indentation (2 spaces)
# Use quotes for descriptions with special characters
# Use | for multi-line descriptions
# Use consistent naming conventions
```

## 🏷️ Tags and Meta Properties

### Using Tags
```yaml
models:
  - name: stg_customers
    tags: ["staging", "pii", "daily"]
    # Run with: dbt run --select tag:staging
```

### Using Meta Properties
```yaml
models:
  - name: dim_customers
    meta:
      owner: "analytics-team"
      slack_channel: "#data-questions"
      business_owner: "marketing-team"
      contains_pii: true
      refresh_schedule: "daily"
```

## 🔧 Configuration Properties

### Model-level Config
```yaml
models:
  - name: fct_orders
    config:
      materialized: incremental
      unique_key: order_id
      on_schema_change: "fail"
      pre-hook: "{{ log('Starting fct_orders build') }}"
      post-hook: "ANALYZE TABLE {{ this }}"
      tags: ["finance", "daily"]
```

### Project-level Config (dbt_project.yml)
```yaml
models:
  jaffle_shop:
    staging:
      +materialized: view
      +tags: ["staging"]
    marts:
      +materialized: table  
      +tags: ["production"]
      finance:
        +materialized: incremental
```

## 🎯 Common YAML Patterns

### Environment-Specific Config
```yaml
models:
  - name: large_fact_table
    config:
      materialized: "{{ 'table' if target.name == 'prod' else 'view' }}"
      dist: "{{ 'customer_id' if target.name == 'prod' else none }}"
```

### Conditional Tests
```yaml
models:
  - name: stg_orders
    columns:
      - name: order_date
        tests:
          - not_null
          - "{{ 'dbt_utils.recency' if target.name == 'prod' else none }}":
              datepart: day
              field: order_date
              interval: 1
```

## ⚠️ Common Mistakes to Avoid

1. **❌ Missing version**: Always include `version: 2`
2. **❌ Inconsistent indentation**: Use 2 spaces consistently
3. **❌ Missing quotes**: Quote special characters and reserved words
4. **❌ Overly complex nesting**: Keep it readable
5. **❌ Duplicate names**: Each resource name must be unique
6. **❌ Missing descriptions**: Every model and column should have a description

## 🔗 Next Steps

- **[Markdown Documentation](markdown-docs.md)** - Learn to write rich descriptions
- **[Interactive Documentation](interactive-docs.md)** - Generate beautiful docs sites

---

**Pro Tip**: Use YAML validation tools and dbt's built-in parsing to catch syntax errors early! 🛠️
