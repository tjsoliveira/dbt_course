# 🧪 Unit Tests in dbt

## 🎯 What are Unit Tests?

**Unit tests** in dbt are a feature that allows you to test **specific transformations** of your models in an **isolated and controlled** way. Unlike traditional data tests, which verify data quality after execution, unit tests:

- **Test transformation logic** with controlled input data
- **Validate calculations and business rules** specifically
- **Execute quickly** without depending on large datasets
- **Facilitate development** and model debugging

## 🔍 How They Work

A unit test in dbt:

1. **Defines input data** (fixtures) for the model
2. **Executes the model** with this controlled data
3. **Compares the result** with the expected output
4. **Reports success or failure** based on the comparison

## 📝 Basic Syntax

```yaml
# models/schema.yml or tests/unit/my_unit_tests.yml
unit_tests:
  - name: test_customer_segmentation
    model: fct_orders
    given:
      - input: ref('stg_customers')
        rows:
          - {customer_id: 1, first_name: "John", email: "john@email.com"}
          - {customer_id: 2, first_name: "Maria", email: "maria@email.com"}
      - input: ref('stg_orders')
        rows:
          - {order_id: 100, customer_id: 1, total_amount: 250.0}
          - {order_id: 101, customer_id: 2, total_amount: 50.0}
    expect:
      rows:
        - {order_id: 100, customer_id: 1, customer_segment: "premium"}
        - {order_id: 101, customer_id: 2, customer_segment: "budget"}
```

## 🏗️ Detailed Structure

### **1. Basic Configuration**
```yaml
unit_tests:
  - name: test_name               # Descriptive test name
    model: model_name             # Model to be tested
    description: "Description..." # Test documentation (optional)
```

### **2. Input Data (given)**
```yaml
given:
  - input: ref('dependency_model')
    rows:
      - {column1: value1, column2: value2}
      - {column1: value3, column2: value4}
  
  - input: source('schema', 'table')  # For sources
    rows:
      - {column_a: valueA, column_b: valueB}
```

### **3. Expected Result (expect)**
```yaml
expect:
  rows:
    - {result_column1: expected_value1, result_column2: expected_value2}
    - {result_column1: expected_value3, result_column2: expected_value4}
```

## 🎯 Practical Use Cases in Jaffle Shop

### **1. Customer Segmentation Test**

**Model:** `fct_orders.sql` - Segmentation logic by order value

```yaml
# tests/unit/test_customer_segmentation.yml
unit_tests:
  - name: test_customer_segmentation_logic
    model: fct_orders
    description: "Tests if customer segmentation works correctly"
    given:
      - input: ref('stg_customers')
        rows:
          - {customer_id: 1, first_name: "Ana", last_name: "Silva", email: "ana@email.com", city: "São Paulo", state: "SP", has_valid_email: true, has_valid_phone: true}
          - {customer_id: 2, first_name: "Bruno", last_name: "Costa", email: "bruno@email.com", city: "Rio de Janeiro", state: "RJ", has_valid_email: true, has_valid_phone: false}
          - {customer_id: 3, first_name: "Carla", last_name: "Mendes", email: "carla@email.com", city: "Belo Horizonte", state: "MG", has_valid_email: false, has_valid_phone: true}
      
      - input: ref('stg_orders')
        rows:
          - {order_id: 100, customer_id: 1, order_date: "2024-01-15", status: "delivered", total_amount: 250.0, payment_method: "credit_card", delivery_address: "Rua A, 123", is_high_value_order: false, is_fulfilled: true, created_at: "2024-01-15 10:00:00"}
          - {order_id: 101, customer_id: 2, order_date: "2024-01-16", status: "shipped", total_amount: 75.0, payment_method: "pix", delivery_address: "Rua B, 456", is_high_value_order: false, is_fulfilled: true, created_at: "2024-01-16 11:00:00"}
          - {order_id: 102, customer_id: 3, order_date: "2024-01-17", status: "processing", total_amount: 350.0, payment_method: "boleto", delivery_address: "Rua C, 789", is_high_value_order: false, is_fulfilled: false, created_at: "2024-01-17 12:00:00"}
      
      - input: ref('stg_items')
        rows:
          - {order_id: 100, quantity: 2, calculated_total_price: 250.0}
          - {order_id: 101, quantity: 1, calculated_total_price: 75.0}
          - {order_id: 102, quantity: 3, calculated_total_price: 350.0}
    
    expect:
      rows:
        - {order_id: 100, customer_id: 1, customer_segment: "premium"}  # 250 > 200
        - {order_id: 101, customer_id: 2, customer_segment: "budget"}   # 75 <= 100
        - {order_id: 102, customer_id: 3, customer_segment: "premium"}  # 350 > 200
```

### **2. Pricing Status Test**

```yaml
# tests/unit/test_pricing_status.yml
unit_tests:
  - name: test_pricing_status_logic
    model: fct_orders
    description: "Tests the logic for comparing original vs calculated prices"
    given:
      - input: ref('stg_customers')
        rows:
          - {customer_id: 1, first_name: "João", last_name: "Santos", email: "joao@email.com", city: "Salvador", state: "BA", has_valid_email: true, has_valid_phone: true}
      
      - input: ref('stg_orders')
        rows:
          - {order_id: 200, customer_id: 1, order_date: "2024-01-20", status: "delivered", total_amount: 100.0, payment_method: "credit_card", delivery_address: "Rua D, 321", is_high_value_order: false, is_fulfilled: true, created_at: "2024-01-20 14:00:00"}
          - {order_id: 201, customer_id: 1, order_date: "2024-01-21", status: "delivered", total_amount: 150.0, payment_method: "pix", delivery_address: "Rua E, 654", is_high_value_order: false, is_fulfilled: true, created_at: "2024-01-21 15:00:00"}
          - {order_id: 202, customer_id: 1, order_date: "2024-01-22", status: "delivered", total_amount: 200.0, payment_method: "boleto", delivery_address: "Rua F, 987", is_high_value_order: false, is_fulfilled: true, created_at: "2024-01-22 16:00:00"}
      
      - input: ref('stg_items')
        rows:
          - {order_id: 200, quantity: 1, calculated_total_price: 120.0}  # Overcharged
          - {order_id: 201, quantity: 1, calculated_total_price: 130.0}  # Undercharged
          - {order_id: 202, quantity: 1, calculated_total_price: 200.0}  # Accurate
    
    expect:
      rows:
        - {order_id: 200, customer_id: 1, pricing_status: "overcharged", has_amount_discrepancy: true}
        - {order_id: 201, customer_id: 1, pricing_status: "undercharged", has_amount_discrepancy: true}
        - {order_id: 202, customer_id: 1, pricing_status: "accurate", has_amount_discrepancy: false}
```

### **3. Phone Cleanup Macro Test**

```yaml
# tests/unit/test_clean_phone_macro.yml
unit_tests:
  - name: test_clean_phone_functionality
    model: stg_customers
    description: "Tests if the clean_phone macro removes special characters correctly"
    given:
      - input: ref('raw_customers')
        rows:
          - {id: 1, first_name: "Ana", last_name: "Silva", email: "ana@email.com", phone: "(11) 99999-9999", address: "Rua A", city: "São Paulo", state: "SP", zip_code: "01000-000", created_at: "2024-01-01", updated_at: "2024-01-01"}
          - {id: 2, first_name: "Bruno", last_name: "Costa", email: "bruno@email.com", phone: "+55 21 8888-8888", address: "Rua B", city: "Rio de Janeiro", state: "RJ", zip_code: "20000-000", created_at: "2024-01-02", updated_at: "2024-01-02"}
          - {id: 3, first_name: "Carla", last_name: "Mendes", email: "carla@email.com", phone: "31.7777.7777", address: "Rua C", city: "Belo Horizonte", state: "MG", zip_code: "30000-000", created_at: "2024-01-03", updated_at: "2024-01-03"}
    
    expect:
      rows:
        - {customer_id: 1, phone: "11999999999", has_valid_phone: true}
        - {customer_id: 2, phone: "5521888888888", has_valid_phone: true}
        - {customer_id: 3, phone: "3177777777", has_valid_phone: true}
```

### **4. Negative Amount Handling Test**

```yaml
# tests/unit/test_negative_amount_handling.yml
unit_tests:
  - name: test_negative_amount_conversion
    model: stg_orders
    description: "Tests if negative values are converted to zero"
    given:
      - input: ref('raw_orders')
        rows:
          - {id: 1, customer_id: 100, order_date: "2024-01-01", status: "delivered", total_amount: -50.0, payment_method: "credit_card", delivery_address: "Rua A", created_at: "2024-01-01"}
          - {id: 2, customer_id: 101, order_date: "2024-01-02", status: "shipped", total_amount: 100.0, payment_method: "pix", delivery_address: "Rua B", created_at: "2024-01-02"}
          - {id: 3, customer_id: 102, order_date: "2024-01-03", status: "processing", total_amount: 0.0, payment_method: "boleto", delivery_address: "Rua C", created_at: "2024-01-03"}
    
    expect:
      rows:
        - {order_id: 1, customer_id: 100, total_amount: 0.0, is_high_value_order: false}
        - {order_id: 2, customer_id: 101, total_amount: 100.0, is_high_value_order: false}
        - {order_id: 3, customer_id: 102, total_amount: 0.0, is_high_value_order: false}
```

## 🚀 How to Run Unit Tests

### **Basic Commands**
```bash
# Run all unit tests
dbt test --select test_type:unit

# Run unit tests for a specific model
dbt test --select fct_orders,test_type:unit

# Run a specific unit test
dbt test --select test_customer_segmentation_logic

# Run with verbosity
dbt test --select test_type:unit --verbose
```

### **During Development**
```bash
# Compile and verify test without executing
dbt compile --select test_customer_segmentation_logic

# Run specific test during development
dbt test --select test_customer_segmentation_logic --store-failures
```

## 🎛️ Advanced Configurations

### **1. Configure Severity**
```yaml
unit_tests:
  - name: test_critical_logic
    model: fct_orders
    config:
      severity: error  # or warn
    given: # ...
    expect: # ...
```

### **2. Tags for Organization**
```yaml
unit_tests:
  - name: test_business_logic
    model: fct_orders
    config:
      tags: ["business_logic", "critical"]
    given: # ...
    expect: # ...
```

### **3. Store Failures**
```yaml
unit_tests:
  - name: test_complex_calculation
    model: fct_orders
    config:
      store_failures: true
    given: # ...
    expect: # ...
```

## 💡 Best Practices

### **1. Execution Environments** ⚠️
```bash
# ✅ Development - Run unit tests freely
dbt test --select test_type:unit

# ✅ CI/CD - Include unit tests in pipeline
dbt test --select test_type:unit --fail-fast

# ❌ Production - AVOID running unit tests
# Reasons:
# - Input data is static (doesn't change)
# - Wastes computational resources
# - Increases costs unnecessarily
# - Adds no value in production runtime
```

### **2. Clear Naming**
```yaml
# ✅ Good: Describes what is being tested
- name: test_customer_segmentation_premium_threshold
- name: test_pricing_status_overcharged_scenario
- name: test_phone_cleanup_special_characters

# ❌ Bad: Generic or unclear
- name: test_orders
- name: test_1
- name: test_model
```

### **3. Minimal Input Data**
```yaml
# ✅ Good: Only necessary columns for the test
given:
  - input: ref('stg_orders')
    rows:
      - {order_id: 1, total_amount: 250.0}
      - {order_id: 2, total_amount: 75.0}

# ❌ Bad: Too many unnecessary columns
given:
  - input: ref('stg_orders')
    rows:
      - {order_id: 1, customer_id: 100, order_date: "2024-01-01", status: "delivered", total_amount: 250.0, payment_method: "credit_card", delivery_address: "Rua A", is_high_value_order: false, is_fulfilled: true, created_at: "2024-01-01 10:00:00"}
```

### **4. Edge Cases**
```yaml
# Test boundary values and special cases
given:
  - input: ref('stg_orders')
    rows:
      - {order_id: 1, total_amount: 200.0}   # Exactly at premium threshold
      - {order_id: 2, total_amount: 200.01}  # Just above threshold
      - {order_id: 3, total_amount: 199.99}  # Just below threshold
      - {order_id: 4, total_amount: 0.0}     # Zero value
      - {order_id: 5, total_amount: null}    # Null value
```

### **5. Test Documentation**
```yaml
unit_tests:
  - name: test_customer_segmentation_logic
    description: |
      Tests customer segmentation logic based on order value:
      - premium: total_amount > 200
      - regular: 100 < total_amount <= 200  
      - budget: total_amount <= 100
      
      Test cases:
      - Exact values at boundaries
      - Values above and below boundaries
      - Edge cases (zero, null)
```

## 🔄 CI/CD Integration

> **⚠️ Important Recommendation from dbt Labs:**
> 
> Run unit tests **only in development or CI environments**. Since input data is static, there's no need to use additional compute cycles running them in production.

### **Test Pipeline**
```bash
# .github/workflows/dbt.yml
- name: Run unit tests (Development/CI only)
  run: |
    dbt deps
    dbt test --select test_type:unit
    
- name: Run integration tests  
  run: |
    dbt run
    dbt test --exclude test_type:unit
```

### **Quick Verification**
```bash
# Quick verification script before commit
#!/bin/bash
echo "Running unit tests..."
dbt test --select test_type:unit --fail-fast

if [ $? -eq 0 ]; then
    echo "✅ All unit tests passed!"
else
    echo "❌ Some unit tests failed!"
    exit 1
fi
```

## 🎯 Benefits of Unit Tests

### **1. Faster Development**
- **Immediate feedback** on code changes
- **Easier debugging** with controlled data
- **Isolated validation** of specific logic

### **2. Greater Confidence**
- **Edge case coverage** before production
- **Living documentation** of expected behavior
- **Regression prevention** during refactoring

### **3. Maintainability**
- **Fast tests** that don't depend on large datasets
- **Failure isolation** in specific logic
- **Safe changes** with confidence

## 📊 Comparison: Unit Tests vs Data Tests

| Aspect | Unit Tests | Data Tests |
|---------|------------|------------|
| **Focus** | Transformation logic | Data quality |
| **Data** | Controlled fixtures | Real/production data |
| **Speed** | ⭐⭐⭐⭐⭐ Very fast | ⭐⭐⭐ Moderate |
| **Isolation** | ⭐⭐⭐⭐⭐ Complete | ⭐⭐ Limited |
| **Coverage** | Specific cases | Complete volume |
| **Usage** | Development/CI | Validation/Production |

## 🎉 Next Steps

1. **Implement unit tests** for critical logic
2. **Add to CI/CD pipelines**
3. **Document test cases** important scenarios
4. **Expand coverage** gradually
5. **Combine with data tests** for complete coverage

---

**Now you're ready to use unit tests in dbt!** 🚀

Start testing simple logic and expand as you gain experience. Remember: unit tests are your safety net for code changes!