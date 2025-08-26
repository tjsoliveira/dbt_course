# Generic Tests

This directory contains reusable generic tests that can be applied to any model to validate data quality. These tests are designed to catch the same types of problems that our data generation scripts create.

## 🧪 Available Tests

### **Order Amount Problems**
- **`test_negative_amount`**: Tests for negative values in numeric columns
- **`test_zero_amount`**: Tests for zero values in numeric columns
- **`test_suspiciously_high`**: Tests for values above a threshold (default: 10,000)

### **Date Problems**
- **`test_missing_date`**: Tests for NULL values in date columns
- **`test_future_date`**: Tests for dates in the future

### **Status Problems**
- **`test_missing_status`**: Tests for NULL values in status columns

### **Customer Data Problems**
- **`test_invalid_customer_email`**: Tests for all email problems defined in config.py
  - `no_at_symbol`: Missing @ symbol
  - `no_domain`: Missing domain part
  - `no_username`: Missing username part
  - `incomplete_domain`: Domain ends with @
  - `no_at_with_domain`: Has .com but no @
  - `empty_string`: Empty email
  - `null_value`: NULL email

- **`test_invalid_customer_phone`**: Tests for all phone problems defined in config.py
  - `too_short`: Less than 10 characters
  - `too_long`: More than 15 characters
  - `with_letters`: Contains letters
  - `only_zeros`: Only zero digits
  - `only_nines`: Only nine digits
  - `wrong_format`: Invalid format
  - `empty_string`: Empty phone
  - `null_value`: NULL phone

### **Product Problems**
- **`test_invalid_product_price`**: Tests for all price problems defined in config.py
  - `missing_price`: NULL price
  - `negative_price`: Negative value
  - `zero_price`: Zero value
  - `extremely_high_price`: Above 100,000
  - `suspiciously_high`: Above 10,000

## 📋 How to Use

### 1. **Basic Usage**
```yaml
# In your model's YAML file
models:
  - name: your_model_name
    tests:
      - test_negative_amount:
          column_name: amount_column
      - test_missing_date:
          column_name: date_column
```

### 2. **With Custom Thresholds**
```yaml
# For tests that support thresholds
models:
  - name: your_model_name
    tests:
      - test_suspiciously_high:
          column_name: price_column
          threshold: 5000  # Custom threshold
```

### 3. **Multiple Tests on Same Column**
```yaml
# Test multiple aspects of the same column
models:
  - name: your_model_name
    tests:
      - test_negative_amount:
          column_name: total_amount
      - test_zero_amount:
          column_name: total_amount
      - test_suspiciously_high:
          column_name: total_amount
          threshold: 10000
```

## 🎯 Test Coverage

These generic tests cover **100%** of the problems that our scripts generate and that the `problematic_orders` model identifies:

### **Order Problems** (from problematic_orders.sql)
- ✅ **`negative_amount`**: `test_negative_amount`
- ✅ **`zero_amount`**: `test_zero_amount`
- ✅ **`missing_date`**: `test_missing_date`
- ✅ **`missing_status`**: `test_missing_status`
- ✅ **`suspiciously_high`**: `test_suspiciously_high`
- ✅ **`future_date`**: `test_future_date`

### **Customer Problems**
- ✅ **Invalid emails**: `test_invalid_customer_email`
- ✅ **Invalid phones**: `test_invalid_customer_phone`

### **Product Problems**
- ✅ **Invalid prices**: `test_invalid_product_price`

## 🚀 Running Tests

```bash
# Run all tests
dbt test

# Run only generic tests
dbt test --select generic

# Run specific generic test
dbt test --select test_negative_amount

# Run tests for specific model
dbt test --select stg_orders
```

## 📊 Expected Results

When tests pass (return 0 rows), it means:
- No data quality problems were found
- All data meets the validation criteria

When tests fail (return > 0 rows), it means:
- Data quality problems were found
- The returned rows show the problematic data with issue_type
- Use this information to fix data generation or data processing

## 🔍 Test Results Analysis

Each test returns:
- **The problematic value**: The actual value that failed the test
- **The issue type**: A clear description of what's wrong

Example output:
```
| total_amount | issue_type      |
|--------------|-----------------|
| -150.50      | negative_amount |
| 0            | zero_amount     |
| 25000        | suspiciously_high|
```

## 🔧 Customization

### **Adding New Problem Types**
1. Create a new generic test file
2. Add the test to the `generic_tests.yml` configuration
3. Update the data generation scripts if needed

### **Modifying Thresholds**
```yaml
# Example: Change suspiciously high threshold
- test_suspiciously_high:
    column_name: total_amount
    threshold: 5000  # Custom threshold instead of default 10000
```

## 🎉 Benefits

1. **Modular**: Each test focuses on one specific problem type
2. **Reusable**: Can be applied to any model with similar columns
3. **Configurable**: Thresholds and parameters can be customized
4. **Consistent**: Same logic across all models
5. **Maintainable**: Easy to update test logic in one place
6. **Comprehensive**: Covers all problem types from our data generation scripts
