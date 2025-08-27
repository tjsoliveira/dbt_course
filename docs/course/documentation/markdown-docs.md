# 📝 Markdown Documentation in dbt

dbt supports rich Markdown formatting in descriptions, allowing you to create beautiful, informative documentation. This guide covers how to leverage Markdown effectively in your dbt project.

## 🎯 What You'll Learn

- ✅ **Markdown Basics**: Formatting text in dbt descriptions
- ✅ **Advanced Features**: Tables, code blocks, and lists
- ✅ **dbt References**: Linking models, sources, and metrics
- ✅ **Jinja in Docs**: Dynamic documentation with Jinja
- ✅ **Best Practices**: Creating maintainable documentation

## 📖 Markdown in dbt Descriptions

### Basic Text Formatting

```yaml
models:
  - name: customer_metrics
    description: |
      # Customer Analytics Dashboard
      
      This model provides **key customer metrics** for the analytics dashboard.
      
      *Last updated*: {{ run_started_at.strftime('%Y-%m-%d') }}
      
      ## Key Metrics Included
      
      - Customer acquisition cost (CAC)
      - Customer lifetime value (CLV) 
      - Monthly recurring revenue (MRR)
      - Churn rate
      
      > **Note**: All monetary values are in USD
```

### Lists and Structure

```yaml
- name: order_summary
  description: |
    ## Order Summary Model
    
    ### Data Sources
    1. `{{ ref('stg_orders') }}` - Raw order data
    2. `{{ ref('stg_customers') }}` - Customer information  
    3. `{{ ref('stg_products') }}` - Product catalog
    
    ### Business Rules
    - Orders must have a valid customer_id
    - Order amounts must be positive
    - Cancelled orders are excluded from revenue calculations
    
    ### Quality Checks
    - [x] No duplicate order IDs
    - [x] All orders have valid dates
    - [x] Customer references exist
    - [ ] Product references validated (pending)
```

## 🔗 dbt References and Links

### Model References

```yaml
models:
  - name: fct_orders
    description: |
      ## Fact Table: Orders
      
      Central fact table containing all order transactions.
      
      **Upstream Dependencies:**
      - {{ ref('stg_customers') }}
      - {{ ref('stg_products') }}
      
      **Downstream Usage:**
      - {{ ref('customer_metrics') }}
      - {{ ref('product_performance') }}
      
      See also: {{ ref('dim_customers') }} for customer dimensions.
```

### Source References

```yaml
sources:
  - name: ecommerce
    tables:
      - name: orders
        description: |
          Raw order data from the e-commerce platform.
          
          **Related Models:**
          - Staging: {{ ref('stg_orders') }}
          - Analytics: {{ ref('fct_orders') }}
          
          **Source Documentation:** {{ source('ecommerce', 'orders') }}
```

### Documentation Blocks

Create reusable documentation blocks:

```yaml
# In models/docs.md or any .md file in your project
<!-- docs tag example -->
## Staging Orders Overview

The staging orders model performs the following transformations:

1. **Data Cleaning:**
   - Remove test orders (order_id < 0)
   - Standardize currency codes
   - Parse order dates

2. **Business Logic:**
   - Calculate order totals including tax
   - Determine order status based on fulfillment
   - Add customer tenure at time of order

3. **Data Quality:**
   - Validate all orders have customers
   - Check for reasonable order amounts
   - Ensure dates are within expected ranges

<!-- enddocs -->
```

Then reference it in YAML:

```yaml
models:
  - name: stg_orders
    description: "[see documentation]"
```


## 🎨 Advanced Formatting

### Alerts and Callouts

```yaml
description: |
  # Data Quality Dashboard
  
  > ⚠️ **Warning**: This model includes data quality checks that may fail during upstream issues.
  
  > ℹ️ **Info**: Refresh schedule is daily at 6 AM UTC.
  
  > ✅ **Success**: All tests passing as of last run.
  
  > 🚨 **Critical**: Contains PII - follow data governance policies.
```

### Badges and Status

```yaml
description: |
  # Customer Analytics ![Status](https://img.shields.io/badge/status-production-green)
  
  ![Last Updated](https://img.shields.io/badge/updated-daily-blue)
  ![Owner](https://img.shields.io/badge/owner-analytics--team-purple)
  
  ## Model Status
  - **Build Status**: ✅ Passing
  - **Test Status**: ✅ All tests pass  
  - **Freshness**: ✅ Updated hourly
  - **Usage**: 📊 High (15+ downstream models)
```

## 📁 Documentation File Organization

### Standalone Documentation Files

Create `.md` files in your project:

```
models/
├── docs/
│   ├── overview.md
│   ├── business_logic.md
│   ├── data_quality.md
│   └── glossary.md
├── staging/
│   └── schema.yml
└── marts/
    └── schema.yml
```

### Business Logic Documentation

```markdown
## Order Status Determination

Orders are classified into the following statuses:

### Status Definitions

1. **Pending** (`pending`)
   - Order placed but payment not processed
   - Inventory not yet allocated
   - Duration: 0-2 hours typical

2. **Confirmed** (`confirmed`) 
   - Payment successful
   - Inventory allocated
   - Ready for fulfillment

3. **Shipped** (`shipped`)
   - Order handed to carrier
   - Tracking number assigned
   - Customer notified

4. **Delivered** (`delivered`)
   - Package delivered to customer
   - Delivery confirmed by carrier
   - Customer satisfaction survey sent

5. **Cancelled** (`cancelled`)
   - Order cancelled by customer or system
   - Inventory released
   - Refund processed if applicable

### Business Rules

- Orders auto-cancel after 24 hours if payment fails
- Express orders skip `confirmed` status when inventory is available
- International orders require additional compliance checks

```

## 🔧 Best Practices

### 1. Structure Your Documentation

```yaml
description: |
  # Model Name
  
  ## Purpose
  Brief description of what this model does
  
  ## Business Logic  
  Key transformations and calculations
  
  ## Data Sources
  Upstream dependencies
  
  ## Usage
  How this model is used downstream
  
  ## Notes
  Important considerations
```

### 2. Keep It Updated

```yaml
# Use Jinja to show freshness
description: |
  **Last Updated**: {{ run_started_at.strftime('%Y-%m-%d') }}
  **Version**: {{ var('model_version', '1.0') }}
```

### 3. Include Examples

```yaml
description: |
  ## Sample Data
  
  | customer_id | order_count | total_revenue |
  |-------------|-------------|---------------|
  | 1001 | 5 | $1,250.00 |
  | 1002 | 12 | $3,480.50 |
  | 1003 | 2 | $89.99 |
```

### 4. Link Related Resources

```yaml
description: |
  **Related Models:**
  - {{ ref('stg_orders') }} - Source data
  - {{ ref('customer_metrics') }} - Uses this model
  
  **Documentation:**
  - [see documentation]
  - [Business Requirements](https://confluence.company.com/orders)
```

## 🎯 Common Patterns

### Model Template

```yaml
models:
  - name: model_name
    description: |
      # {{ model_name | title }}
      
      **Owner**: {{ var('team_name') }}
      **Updated**: {{ run_started_at.strftime('%Y-%m-%d') }}
      
      ## Purpose
      Brief description of model purpose
      
      ## Key Metrics
      - Metric 1: Description
      - Metric 2: Description
      
      ## Dependencies
      - {{ ref('upstream_model') }}
      
      ## Usage
      Used by {{ ref('downstream_model') }}
      
    columns:
      - name: id
        description: "Primary key"
        tests: [unique, not_null]
```

## 🔗 Next Steps

- **[Interactive Documentation](interactive-docs.md)** - Generate beautiful docs sites
- **[YAML Configuration](yaml-configuration.md)** - Back to YAML basics

---

**Pro Tip**: Use documentation blocks for content you'll reuse across multiple models! 📚
