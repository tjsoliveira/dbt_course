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
      - {{ doc('staging_orders_overview') }}
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
{% docs staging_orders_overview %}
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

**Sample Query:**
```sql
SELECT 
    order_id,
    customer_id, 
    order_total,
    order_date,
    status
FROM {{ ref('stg_orders') }}
WHERE order_date >= '2024-01-01'
LIMIT 10;
```
{% enddocs %}
```

Then reference it in YAML:

```yaml
models:
  - name: stg_orders
    description: "{{ doc('staging_orders_overview') }}"
```

## 📊 Tables and Data Examples

### Creating Tables

```yaml
- name: customer_segments
  description: |
    ## Customer Segmentation Model
    
    | Segment | CLV Range | Characteristics |
    |---------|-----------|----------------|
    | Premium | $1000+ | High engagement, frequent purchases |
    | Standard | $200-999 | Regular customers, moderate spend |
    | Basic | $0-199 | New or low-engagement customers |
    
    ### Segment Distribution
    
    | Segment | Count | Percentage |
    |---------|-------|------------|
    | Premium | 1,234 | 12.3% |
    | Standard | 5,678 | 56.8% |
    | Basic | 3,088 | 30.9% |
```

### Code Examples

```yaml
- name: revenue_metrics
  description: |
    ## Revenue Calculation Logic
    
    ### Monthly Recurring Revenue (MRR)
    ```sql
    SUM(
      CASE 
        WHEN subscription_type = 'monthly' THEN amount
        WHEN subscription_type = 'annual' THEN amount / 12
        ELSE 0 
      END
    ) AS mrr
    ```
    
    ### Customer Acquisition Cost (CAC)
    ```sql
    marketing_spend / new_customers AS cac
    ```
    
    ### Example Usage
    ```sql
    SELECT 
        date_month,
        mrr,
        cac,
        mrr / cac AS ltv_cac_ratio
    FROM {{ ref('revenue_metrics') }}
    WHERE date_month >= '2024-01-01';
    ```
```

## 🧩 Jinja in Documentation

### Dynamic Content

```yaml
models:
  - name: daily_summary
    description: |
      # Daily Business Summary
      
      **Generated**: {{ run_started_at.strftime('%Y-%m-%d %H:%M UTC') }}
      **Environment**: {{ target.name }}
      **Database**: {{ target.database }}
      
      {% if target.name == 'prod' %}
      > ⚠️ **Production Data** - Handle with care
      {% else %}
      > 🧪 **Development Environment** - Safe for testing
      {% endif %}
```

### Conditional Documentation

```yaml
- name: sensitive_data
  description: |
    # Customer Personal Data
    
    {% if target.name == 'prod' %}
    **⚠️ CONTAINS PII - RESTRICTED ACCESS**
    
    This model contains personally identifiable information including:
    - Full names
    - Email addresses  
    - Phone numbers
    - Billing addresses
    
    **Access Policy**: Data team and compliance team only
    **Retention**: 7 years per GDPR requirements
    {% else %}
    **🔒 Masked Development Data**
    
    In non-production environments, all PII fields are masked or synthetic.
    {% endif %}
```

### Macros in Documentation

```yaml
- name: financial_metrics
  description: |
    # Financial Performance Metrics
    
    **Calculation Period**: {{ dbt_utils.pretty_time('%Y-%m-%d') }}
    
    ## Revenue Recognition Rules
    
    {{ doc('revenue_recognition_policy') }}
    
    ## Key Formulas
    
    {% for metric in ['arr', 'mrr', 'churn_rate'] %}
    - **{{ metric | title }}**: {{ doc(metric + '_calculation') }}
    {% endfor %}
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

### Diagrams and Flowcharts

```yaml
description: |
  # Order Processing Pipeline
  
  ```mermaid
  graph TD
      A[Raw Orders] --> B[Data Validation]
      B --> C[Business Logic]
      C --> D[Quality Checks]
      D --> E[Final Orders]
      
      F[Customer Data] --> C
      G[Product Data] --> C
  ```
  
  ## Process Flow
  1. **Ingestion** - Raw order data from API
  2. **Validation** - Check required fields
  3. **Enrichment** - Add customer and product info
  4. **Calculation** - Apply business rules
  5. **Output** - Clean, enriched order facts
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
<!-- models/docs/business_logic.md -->
{% docs order_status_logic %}
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

{% enddocs %}
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
  - {{ doc('order_processing_overview') }}
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
