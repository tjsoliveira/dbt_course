# 🛠️ Environment Setup

In this section, you'll learn how to set up your development environment to work with dbt and the Jaffle Shop project.

## 📋 Prerequisites

Before starting, make sure you have installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **Code editor** - We recommend [VS Code](https://code.visualstudio.com/) or [PyCharm](https://www.jetbrains.com/pycharm/)

## 🚀 Quick Start (Recommended)

The easiest way to get started is using our automated setup script:

```bash
# Clone the repository
git clone https://github.com/tjsoliveira/dbt_course.git
cd dbt_course

# Run the automated setup script
./init_project.sh
```

- This script will:
  - ✅ Set up Python virtual environment
  - ✅ Install all required dependencies
  - ✅ Configure dbt project
  - ✅ Generate sample data
  - ✅ Verify installation

## 🐍 Manual Python Installation

### Windows
1. **Download Python**: Go to [python.org/downloads](https://www.python.org/downloads/)
2. **Download the latest Python 3.x** (3.8 or higher)
3. **Run the installer** with these important settings:
    - ✅ **Check "Add Python to PATH"** (very important!)
    - ✅ **Check "pip"** (package installer)
    - ✅ Choose "Install for all users" (recommended)
4. **Verify installation**:
```cmd
# Open Command Prompt (cmd) or PowerShell and run:
python --version
pip --version
```
### macOS
```bash
# Using Homebrew
brew install python

# Or download the installer from Python.org
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

## 🔧 Manual dbt Setup

If you prefer to set up manually or the automated script doesn't work:

### 1. Create Virtual Environment

```bash
# Create project directory
mkdir dbt_course
cd dbt_course

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# Install all project requirements
pip install -r requirements.txt

# This includes:
# - dbt-core
# - dbt-sqlite (for Jaffle Shop)
# - faker (for data generation)
# - pandas (for data operations)
```

### 3. Verify Installation

```bash
dbt --version
```

## 🗄️ Database Configuration

This course uses **SQLite** for simplicity - no server setup required!

The database configuration is already included in the project:

```yaml
# profiles.yml (already configured)
jaffle_shop:
  target: dev
  outputs:
    dev:
      type: sqlite
      path: "jaffle_shop/jaffle_shop.db"
      threads: 1
```

## 📊 Generate Sample Data

The Project includes Python scripts to generate realistic sample data:

### 🚀 Quick Data Generation (Recommended)

```bash
cd jaffle_shop
python scripts/generate_all_data.py
```

**This single command generates:**
- ✅ Customer data (`raw_customers.csv`)
- ✅ Product data (`raw_products.csv`)  
- ✅ Order data (`raw_orders.csv`)
- ✅ Order items data (`raw_items.csv`)
- ✅ Intentional data quality issues for testing
- ✅ Realistic Brazilian data (names, addresses, etc.)

### 📋 Generated Data Features

The data generator creates:

- **Customer Data**: 1000+ customers with realistic Brazilian names, emails, and addresses
- **Product Data**: Comprehensive product catalog with categories and brands
- **Order Data**: Realistic order patterns with dates between 2020-2024
- **Data Quality Issues**: Intentional issues to test your dbt models:
  - Invalid email formats (15% of records)
  - Invalid phone numbers (20% of records)
  - Negative amounts, future dates, missing fields

### 🎯 Individual Data Generation

If you want to generate specific datasets:

```bash
# Generate only customer data
python scripts/generate_customer_data.py -n 2000

# Generate only product data  
python scripts/generate_products_data.py

# Generate only orders and items
python scripts/generate_items_data.py
```

## 📁 Project Structure

After setup, you'll have this structure:

```
dbt_course/
├── jaffle_shop/                 # Main dbt project
│   ├── dbt_project.yml         # dbt configuration
│   ├── profiles.yml            # Database connections
│   ├── models/                 # SQL models
│   │   ├── staging/           # Staging models
│   │   ├── marts/             # Business logic models
│   │   └── analytics/         # Analytical models
│   ├── seeds/                  # Static/generated data
│   │   └── jaffle-data/       # Generated CSV files
│   ├── tests/                  # Custom tests
│   ├── macros/                 # Reusable SQL macros
│   └── scripts/                # Data generation scripts
├── docs/                       # Course documentation
├── requirements.txt            # Python dependencies
└── init_project.sh            # Setup script
```

## 🧪 Verify Everything Works

Run these commands to test your setup:

```bash
cd jaffle_shop

# Test dbt installation
dbt debug

# Load seed data
dbt seed

# Run all models
dbt run

# Run tests
dbt test

# Generate documentation
dbt docs generate
dbt docs serve
```

If all commands run successfully, you're ready to start the course! 🎉

## 🆘 Troubleshooting

### Error: "dbt command not found"
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
```

### Data Generation Issues
```bash
# Install required packages
pip install faker pandas

# Check if you're in the right directory
cd jaffle_shop
ls scripts/  # Should show generate_*.py files
```

### Database Connection Error
```bash
# Check if profiles.yml exists
ls -la profiles.yml

# Run dbt debug for detailed error info
dbt debug
```

### Dependency Errors
```bash
# Upgrade pip and reinstall
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## 📚 Next Steps

1. ✅ **Environment configured** ← You are here
2. [About the Project](../jaffle-shop/overview.md) - Understand the Jaffle Shop
3. [Project Setup](../jaffle-shop/project-setup.md) - Deep dive into dbt project
4. [Start the Course](../course/index.md) - Begin learning dbt

Let's learn about the project: [About the Project](../jaffle-shop/overview.md)!
