# 📊 Sources in dbt

Sources are the foundation of your dbt project. They represent the raw data tables in your data warehouse that serve as inputs to your transformation models.

## 🎯 What are Sources?

**Sources** in dbt are a way to:
- **Document** your raw data tables
- **Test** data quality at the source level
- **Track lineage** from raw data to final models
- **Version control** your data schema expectations
- **Centralize** source table references

Think of sources as the "entry points" to your data transformation pipeline.

## 🏗️ Source Configuration

Sources are defined in YAML files, typically in your `models/` directory or a dedicated `sources/` directory.

### **Basic Source Definition**
```yaml
# models/sources.yml
version: 2

sources:
  - name: jaffle_shop
    description: "Raw data from the Jaffle Shop e-commerce platform"
    tables:
      - name: customers
        description: "Customer information"
      - name: orders  
        description: "Order transactions"
      - name: products
        description: "Product catalog"
```

### **Advanced Source Configuration**
```yaml
version: 2

sources:
  - name: jaffle_shop
    description: "Raw data from the Jaffle Shop e-commerce platform"
    database: raw_data
    schema: jaffle_shop_raw
    
    tables:
      - name: customers
        description: "Customer demographic and contact information"
        columns:
          - name: id
            description: "Primary key for customers"
            tests:
              - unique
              - not_null
          - name: first_name
            description: "Customer first name"
            tests:
              - not_null
          - name: email
            description: "Customer email address"
            tests:
              - not_null
              - unique
        
        tests:
          - dbt_utils.expression_is_true:
              expression: "id > 0"
```

## 🔗 Using Sources in Models

Once defined, sources are referenced using the `source()` function:

### **Basic Source Reference**
```sql
-- models/staging/stg_customers.sql
select
    id as customer_id,
    first_name,
    last_name,
    email,
    created_at
from {{ source('jaffle_shop', 'customers') }}
```

### **Source Reference with Alias**
```sql
-- models/staging/stg_orders.sql
select
    id as order_id,
    user_id as customer_id,
    order_date,
    status,
    total_amount
from {{ source('jaffle_shop', 'orders') }} as raw_orders
where order_date is not null
```

## 📋 Source Properties

### **Required Properties**
- **`name`**: Unique identifier for the source
- **`tables`**: List of tables within the source

### **Optional Properties**
- **`description`**: Human-readable description
- **`database`**: Database name (if different from default)
- **`schema`**: Schema name (if different from default)
- **`loader`**: ETL tool that loads the data (Fivetran, Stitch, etc.)
- **`loaded_at_field`**: Timestamp field indicating when data was loaded

### **Example with All Properties**
```yaml
sources:
  - name: jaffle_shop
    description: "E-commerce platform data"
    database: "{{ target.database }}"
    schema: raw_jaffle_shop
    loader: fivetran
    loaded_at_field: _fivetran_synced
    
    tables:
      - name: customers
        description: "Customer master data"
        identifier: dim_customers  # If table name differs
        columns:
          - name: customer_id
            description: "Unique customer identifier"
```

## 🧪 Testing Sources

Sources support the same tests as models:

### **Column-Level Tests**
```yaml
sources:
  - name: jaffle_shop
    tables:
      - name: customers
        columns:
          - name: id
            tests:
              - unique
              - not_null
          - name: email
            tests:
              - unique
              - not_null
              - dbt_utils.email_validator
```

### **Table-Level Tests**
```yaml
sources:
  - name: jaffle_shop
    tables:
      - name: orders
        tests:
          - dbt_utils.expression_is_true:
              expression: "total_amount >= 0"
          - dbt_utils.at_least_one
```

### **Custom Source Tests**
```yaml
sources:
  - name: jaffle_shop
    tables:
      - name: customers
        tests:
          - assert_customer_data_quality:
              min_customers: 100
```

## 📈 Source Freshness

Monitor how fresh your source data is:

### **Configure Freshness Checks**
```yaml
sources:
  - name: jaffle_shop
    tables:
      - name: orders
        loaded_at_field: created_at
        freshness:
          warn_after: {count: 12, period: hour}
          error_after: {count: 24, period: hour}
```

### **Run Freshness Checks**
```bash
# Check freshness for all sources
dbt source freshness

# Check specific source
dbt source freshness --select source:jaffle_shop

# Check specific table
dbt source freshness --select source:jaffle_shop.orders
```


## 🚀 Best Practices

### **1. Organization**
```yaml
# Option 1: Single sources file
models/sources.yml

# Option 2: Source-specific files
models/sources/
├── jaffle_shop.yml
├── marketing.yml
└── finance.yml

# Option 3: Domain-specific organization
models/
├── staging/
│   └── jaffle_shop/
│       └── sources.yml
└── marts/
```

### **2. Naming Conventions**
- **Source names**: Use the system/platform name (`salesforce`, `stripe`, `jaffle_shop`)
- **Table names**: Use original table names from source system
- **Descriptions**: Always include meaningful descriptions

### **3. Documentation Standards**
```yaml
sources:
  - name: jaffle_shop
    description: |
      ## Jaffle Shop E-commerce Platform
      
      Raw data from our e-commerce platform including:
      - Customer demographics and contact information
      - Order transactions and line items
      - Product catalog with pricing
      
      **Data Quality Notes:**
      - Contains intentional data quality issues for learning
      - Updated daily via CSV seed files
      - Used for dbt training and testing
```

### **4. Testing Strategy**
- **Always test** primary keys (unique + not_null)
- **Test critical fields** that downstream models depend on
- **Use freshness checks** for time-sensitive data
- **Document known issues** in descriptions

## 🔍 Source Commands

### **Essential Commands**
```bash
# List all sources
dbt ls --resource-type source

# Run source tests
dbt test --select source:*

# Test specific source
dbt test --select source:jaffle_shop

# Check source freshness
dbt source freshness

# Compile source references
dbt compile --select source:jaffle_shop.customers
```

### **Advanced Usage**
```bash
# Test sources and downstream models
dbt test --select source:jaffle_shop+

# Run models that depend on a source
dbt run --select source:jaffle_shop.customers+

# Generate source documentation
dbt docs generate --select source:*
```

## 📊 Source vs Seeds vs Models

| Aspect | Sources | Seeds | Models |
|--------|---------|-------|--------|
| **Purpose** | Reference external data | Version control small datasets | Transform data |
| **Data Location** | External database/warehouse | CSV files in project | Created by dbt |
| **Configuration** | YAML only | YAML + CSV | YAML + SQL |
| **Testing** | Column & table tests | Same as models | Column & table tests |
| **Materialization** | Not applicable | Table (automatic) | Configurable |
| **Usage** | `source()` function | `ref()` function | `ref()` function |

## 🎯 When to Use Sources

**✅ Use Sources for:**
- External database tables
- Data warehouse raw tables  
- API endpoints loaded by ETL tools
- Any data not created by dbt

**❌ Don't Use Sources for:**
- CSV files (use seeds instead)
- dbt models (use ref() instead)
- Temporary/staging tables created by dbt

## 🔗 Next Steps

After mastering sources, explore:

1. **Seeds**- Version control small datasets
2. **Staging Models** - Transform sources into clean data
3. **Model Testing** - Comprehensive testing strategies
4. **Documentation** - Document your data pipeline

---

**💡 Remember**: Sources are your data's entry point into dbt. Properly configured sources make your entire pipeline more reliable, testable, and maintainable!