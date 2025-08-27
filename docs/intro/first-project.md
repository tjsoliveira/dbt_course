# 🎯 Creating Your First dbt Project

Now that your environment is configured, let's create your first dbt project! We'll use the Jaffle Shop project as an example.

## 🚀 Initializing the Project

### 1. Create the Project

```bash
# Navigate to the directory where you want to create the project
cd ~/Projects

# Initialize new dbt project
dbt init jaffle_shop

# Navigate to the project
cd jaffle_shop
```

### 2. Initial Structure

After initialization, you'll have:

```
jaffle_shop/
├── dbt_project.yml          # Main configuration
├── profiles.yml             # Connection configurations
├── models/                  # SQL models
│   └── example/             # Example model
├── tests/                   # Tests
├── macros/                  # Macros
├── seeds/                   # Static data
├── snapshots/               # Snapshots
├── target/                  # Compiled files
├── logs/                    # Execution logs
└── README.md                # Project documentation
```

## ⚙️ Project Configuration

### 1. dbt_project.yml

Edit the `dbt_project.yml` file:

```yaml
name: 'jaffle_shop'
version: '1.0.0'
config-version: 2

profile: 'jaffle_shop'

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"
clean-targets:
    - "target"
    - "dbt_packages"

models:
  jaffle_shop:
    staging:
      +materialized: view
    marts:
      +materialized: table
    analytics:
      +materialized: table

seeds:
  jaffle_shop:
    +column_types:
      id: integer
      customer_id: integer
      order_id: integer
      product_id: integer
```

### 2. profiles.yml

Configure the database connection in `~/.dbt/profiles.yml`:

```yaml
jaffle_shop:
  target: dev
  outputs:
    dev:
      type: sqlite
      path: "{{ env_var('DBT_SQLITE_PATH', '/tmp/jaffle_shop.db') }}"
      threads: 1
```

## 🗄️ Preparing the Data

### 1. Create SQLite Database

```bash
# Create SQLite database
sqlite3 /tmp/jaffle_shop.db

# In SQLite shell, create tables
CREATE TABLE raw_customers (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT
);

CREATE TABLE raw_products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    price REAL
);

CREATE TABLE raw_orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    status TEXT
);

CREATE TABLE raw_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price REAL
);

.exit
```

### 2. Insert Sample Data

```bash
# Insert sample data
sqlite3 /tmp/jaffle_shop.db << EOF
INSERT INTO raw_customers VALUES (1, 'John', 'Smith', 'john@email.com', '11999999999');
INSERT INTO raw_customers VALUES (2, 'Mary', 'Johnson', 'mary@email.com', '11888888888');
INSERT INTO raw_customers VALUES (3, 'Peter', 'Brown', 'peter@email.com', '11777777777');

INSERT INTO raw_products VALUES (1, 'Laptop', 'Electronics', 2500.00);
INSERT INTO raw_products VALUES (2, 'Mouse', 'Electronics', 50.00);
INSERT INTO raw_products VALUES (3, 'Table', 'Furniture', 300.00);

INSERT INTO raw_orders VALUES (1, 1, '2024-01-15', 'completed');
INSERT INTO raw_orders VALUES (2, 2, '2024-01-16', 'pending');
INSERT INTO raw_orders VALUES (3, 3, '2024-01-17', 'completed');

INSERT INTO raw_items VALUES (1, 1, 1, 1, 2500.00);
INSERT INTO raw_items VALUES (2, 1, 2, 2, 50.00);
INSERT INTO raw_items VALUES (3, 2, 3, 1, 300.00);
INSERT INTO raw_items VALUES (4, 3, 1, 1, 2500.00);
EOF
```

## 🏗️ Creating Models

### 1. Staging Model

Create `models/staging/stg_customers.sql`:

```sql
{{
  config(
    materialized='view'
  )
}}

SELECT
    id,
    first_name,
    last_name,
    email,
    phone,
    -- Clean and standardize data
    TRIM(first_name) as first_name_clean,
    TRIM(last_name) as last_name_clean,
    LOWER(email) as email_clean,
    -- Validate email
    CASE 
        WHEN email LIKE '%@%' THEN 'valid'
        ELSE 'invalid'
    END as email_status
FROM {{ source('raw', 'raw_customers') }}
```

### 2. Mart Model

Create `models/marts/customer_summary.sql`:

```sql
{{
  config(
    materialized='table'
  )
}}

WITH customer_orders AS (
    SELECT
        c.id as customer_id,
        c.first_name_clean,
        c.last_name_clean,
        c.email_clean,
        COUNT(o.id) as total_orders,
        SUM(CASE WHEN o.status = 'completed' THEN 1 ELSE 0 END) as completed_orders,
        SUM(CASE WHEN o.status = 'pending' THEN 1 ELSE 0 END) as pending_orders
    FROM {{ ref('stg_customers') }} c
    LEFT JOIN {{ ref('stg_orders') }} o ON c.id = o.customer_id
    GROUP BY 1, 2, 3, 4
)

SELECT
    customer_id,
    first_name_clean,
    last_name_clean,
    email_clean,
    total_orders,
    completed_orders,
    pending_orders,
    -- Calculate metrics
    CASE 
        WHEN total_orders > 0 THEN ROUND(completed_orders * 100.0 / total_orders, 2)
        ELSE 0
    END as completion_rate
FROM customer_orders
```

## 🧪 Running the Project

### 1. Verify Configuration

```bash
# Verify everything is configured
dbt debug
```

### 2. Run Models

```bash
# Run all models
dbt run

# Run only staging
dbt run --select staging

# Run only marts
dbt run --select marts
```

### 3. Run Tests

```bash
# Run all tests
dbt test

# Run specific tests
dbt test --select stg_customers
```

### 4. Generate Documentation

```bash
# Generate documentation
dbt docs generate

# Serve documentation locally
dbt docs serve
```

## 📊 Checking Results

### 1. Query Models

```bash
# Check staging
sqlite3 /tmp/jaffle_shop.db "SELECT * FROM stg_customers;"

# Check marts
sqlite3 /tmp/jaffle_shop.db "SELECT * FROM customer_summary;"
```

### 2. Check DAG

```bash
# Generate dependency graph
dbt ls --select +customer_summary
```

## 🎉 Congratulations!

You've successfully created your first dbt project! 🎊

## 📚 Next Steps

1. ✅ **First project created** ← You are here
2. [Explore Jaffle Shop](../jaffle-shop/overview.md)
3. Understand Staging Models
4. Create Mart Models

## 🔍 Useful Commands

```bash
# Check model status
dbt run --models staging

# Run tests
dbt test

# Generate documentation
dbt docs generate

# Clean artifacts
dbt clean

# View logs
dbt run --log-level debug
```

---

**Is your first dbt project working?** 🚀

Let's explore the [Jaffle Shop project](../jaffle-shop/overview.md) in detail!
