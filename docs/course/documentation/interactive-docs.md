# Interactive Documentation with dbt docs

dbt offers a powerful feature to automatically generate interactive documentation from your project. The `dbt docs` command creates a web interface that allows you to navigate through models, tests, sources, and project dependencies in a visual and intuitive way.

## What is Interactive Documentation?

dbt's interactive documentation is a static web application that:

- **Visualizes the lineage** of your models and sources
- **Automatically documents** all tables and columns
- **Shows relationships** between models
- **Displays test results** and validations
- **Enables intuitive navigation** through the project

## Main Commands

### Generating Documentation

```bash
dbt docs generate
```

This command:
- Collects information about models, sources, tests, and macros
- Generates JSON files with project metadata
- Creates the necessary files for the web interface

### Serving Documentation

```bash
dbt docs serve
```

This command:
- Starts a local web server
- Makes documentation available at `http://localhost:8080`
- Enables interactive navigation through the project

### Combined Command

```bash
dbt docs generate && dbt docs serve
```

Executes both commands in sequence to generate and serve the documentation.

## Interface Features

### 1. Lineage Graph

The lineage graph shows:
- **Data sources** (seeds, sources)
- **Intermediate and final models**
- **Dependencies** between models
- **Data flow** through the project

### 2. Model Documentation

For each model, the interface displays:
- **Model description**
- **Columns** and their data types
- **Applied tests**
- **Upstream and downstream dependencies**
- **SQL code** of the model

### 3. Source Documentation

For sources, it shows:
- **Source description**
- **Available tables**
- **Columns** and metadata
- **Configured source tests**

## Configuration in dbt_project.yml

```yaml
# dbt_project.yml
name: 'jaffle_shop'
version: '1.0.0'

# Documentation configurations
docs-paths: ["docs"]

# Assets for documentation
asset-paths: ["assets"]
```

## Adding Descriptions

### In Models

```sql
-- models/customers.sql
{{ config(
    description="Customer dimension table with aggregated metrics"
) }}

select
    customer_id,
    first_name,
    last_name,
    -- Customer's first order date
    first_order_date,
    -- Total value of all orders
    customer_lifetime_value
from {{ ref('stg_customers') }}
```

### In Schema.yml

```yaml
# models/schema.yml
version: 2

models:
  - name: customers
    description: "Customer dimension with aggregated information"
    columns:
      - name: customer_id
        description: "Primary key of the customers table"
        tests:
          - unique
          - not_null
      
      - name: first_name
        description: "Customer's first name"
        tests:
          - not_null
      
      - name: customer_lifetime_value
        description: "Total amount spent by customer across all orders"
```

## Best Practices

### 1. Consistent Documentation

- **Always document** important models
- **Use clear and objective descriptions**
- **Document main columns**
- **Keep updated** with changes

### 2. Tests and Validations

- **Add tests** to models
- **Validate relationships** between tables
- **Test unique and not null** data
- **Document data expectations**

### 3. Visual Organization

- **Use tags** to group models
- **Organize in logical folders**
- **Name consistently**
- **Maintain clear hierarchy**

## Practical Example

Let's document the `customers` model:

```yaml
# models/schema.yml
version: 2

models:
  - name: customers
    description: >
      Dimensional table that aggregates customer information
      with purchase behavior metrics.
    
    columns:
      - name: customer_id
        description: "Unique customer identifier"
        tests:
          - unique
          - not_null
        
      - name: first_name
        description: "Customer's first name"
        tests:
          - not_null
          
      - name: last_name
        description: "Customer's last name"
        tests:
          - not_null
          
      - name: first_order_date
        description: "Date of the customer's first order"
        
      - name: most_recent_order_date
        description: "Date of the customer's most recent order"
        
      - name: number_of_orders
        description: "Total number of orders placed"
        tests:
          - not_null
          
      - name: customer_lifetime_value
        description: "Total amount spent by customer across all orders"
        tests:
          - not_null
```

## Useful Commands

```bash
# Generate documentation only
dbt docs generate

# Serve on specific port
dbt docs serve --port 8001

# Generate docs for specific models
dbt docs generate --models customers

# Include sources in documentation
dbt docs generate --include-sources
```

## Conclusion

dbt's interactive documentation is a fundamental tool for:

- **Understanding** project structure
- **Communicating** about models and transformations
- **Validating** data quality
- **Facilitating** team collaboration
- **Maintaining** organizational knowledge

Use `dbt docs generate && dbt docs serve` to explore your project and always keep documentation up to date!
