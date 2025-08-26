# Data Generator for dbt Project

This project contains Python scripts that generate CSV data using the Faker library, exactly matching the columns of the dbt models.

## 🚀 Main Script (Recommended)

### `generate_all_data.py`
**The easiest way to generate all data at once:**
```bash
python scripts/generate_all_data.py
```

**Advantages:**
- ✅ Generates all data types automatically
- ✅ Pre-configured with optimal settings
- ✅ Includes intentional data quality issues for testing
- ✅ Perfect for testing the `problematic_orders` model
- ✅ Single command execution
- ✅ Detailed execution report

## 📊 Individual Scripts

### 1. generate_customer_data.py
Generates customer data matching the `stg_customers.sql` model.

### 2. generate_items_data.py
Generates related items and orders data, matching the `stg_items.sql` and `stg_orders.sql` models.

### 3. generate_products_data.py
Generates product data with categories, subcategories, and brands, compatible with JOIN in `raw_items.csv`.

## 🎯 Quick Start

**For most users, simply run:**
```bash
cd jaffle_shop
python scripts/generate_all_data.py
```

This will generate all the data you need with one command!

## 📋 Generated Columns

The script generates the following columns that match your SQL model:

- `id` - Unique customer ID
- `first_name` - Customer first name
- `last_name` - Customer last name  
- `email` - Valid customer email
- `phone` - Phone number (can be NULL for some customers)
- `address` - Address
- `city` - Brazilian city
- `state` - Brazilian state (abbreviation)
- `zip_code` - Brazilian postal code
- `created_at` - Creation date
- `updated_at` - Update date

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 🚀 Recommended: Generate All Data
```bash
python scripts/generate_all_data.py
```
Generates all data types with optimal configuration for testing.

### Individual Script Usage

#### Basic Usage
```bash
python scripts/generate_customer_data.py
```
Generates 1000 records and saves to `seeds/jaffle-data/raw_customers.csv`

#### Customize Number of Records
```bash
python scripts/generate_customer_data.py -n 5000
```
Generates 5000 records

#### Customize Output Filename
```bash
python scripts/generate_customer_data.py -o my_customers.csv
```
Saves data to `my_customers.csv`

#### Combine Options
```bash
python scripts/generate_customer_data.py -n 2000 -o customers_2024.csv
```
Generates 2000 records and saves to `customers_2024.csv`

## Data Characteristics

- **Names**: Generated in Brazilian Portuguese
- **Emails**: 85% valid with format `firstname.lastname@domain.com`, 15% invalid to test validation
- **Phones**: 90% of customers have phones, with 80% valid and 20% invalid to test validation
- **Addresses**: Realistic Brazilian addresses
- **Cities and States**: Real Brazilian cities and states
- **Postal Codes**: Valid Brazilian format (00000-000)
- **Dates**: Between 2020 and 2024, with creation/update logic

## Sample Output

```csv
id,first_name,last_name,email,phone,address,city,state,zip_code,created_at,updated_at
1,João,Santos,joao.santos@hotmail.com,(11) 98765-4321,Rua das Flores 123,São Paulo,SP,01234-567,2023-05-15 10:30:00,2024-01-20 14:45:00
2,Maria,Silva,maria.silva@gmail.com,,Avenida Brasil 456,Rio de Janeiro,RJ,20000-123,2022-08-10 09:15:00,2023-12-05 16:20:00
3,Pedro,Oliveira,pedro.oliveira,123,Rua das Palmeiras 789,Curitiba,PR,80000-123,2023-10-12 11:20:00,2024-02-01 09:30:00
```

## Invalid Data for Testing

The script intentionally generates some invalid data to test the validation logic in your SQL model:

### Invalid Emails (15% of records):
- Without at symbol (@): `joao.silva` (simple format without @)

### Invalid Phones (20% of phones):
- Too short: `123`
- Too long: `12345678901234567890`
- With letters: `abc-def-ghij`
- Incorrect formats: `(11) 1234-567`

## Items and Orders Script

### Usage
```bash
python scripts/generate_items_data.py
```

Generates related data for:
- `raw_orders.csv` - Order information
- `raw_items.csv` - Order items with product references

### Features
- Generates realistic order dates
- Calculates total amounts based on items
- Creates relationships between orders and customers
- Generates items with quantities and prices

## Products Script

### Usage
```bash
python scripts/generate_products_data.py
```

### Features
- Generates products with realistic categories
- Creates brand hierarchies
- Generates price ranges
- Ensures referential integrity with items

## Data Quality Issues

The scripts generate intentional data quality issues to test your dbt models:

### Customer Data Issues:
- Invalid email formats
- Invalid phone numbers
- Missing required fields

### Order Data Issues:
- Negative amounts
- Zero amounts
- Future dates
- Missing status

### Product Data Issues:
- Invalid prices
- Missing categories
- Inconsistent brand information

## Testing Your dbt Models

After generating data, you can test your dbt models:

```bash
# Build models
dbt run

# Run tests
dbt test

# Generate documentation
dbt docs generate
```

## Customization

You can modify the scripts to:
- Change data generation patterns
- Add new columns
- Modify validation rules
- Adjust data quality issue percentages

## Requirements

- Python 3.8+
- Faker library
- pandas (for CSV operations)

## Contributing

Feel free to contribute by:
- Adding new data generation patterns
- Improving data quality issues
- Adding new validation tests
- Enhancing documentation
