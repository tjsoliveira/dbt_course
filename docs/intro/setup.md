# 🛠️ Environment Setup

In this section, you'll learn how to set up your development environment to work with dbt.

## 📋 Prerequisites

Before starting, make sure you have installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **Code editor** - We recommend [VS Code](https://code.visualstudio.com/) or [PyCharm](https://www.jetbrains.com/pycharm/)

## 🐍 Python Installation

### Windows
```bash
# Download the installer from Python.org
# Run the installer and check "Add Python to PATH"
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
sudo apt install python3 python3-pip
```

## 🔧 dbt Installation

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

### 2. Install dbt

```bash
# Install dbt Core
pip install dbt-core

# Install adapter for your database
# For SQLite (used in this course)
pip install dbt-sqlite

# For PostgreSQL
pip install dbt-postgres

# For BigQuery
pip install dbt-bigquery

# For Snowflake
pip install dbt-snowflake
```

### 3. Verify Installation

```bash
dbt --version
```

## 🗄️ Database Configuration

### SQLite (Recommended for Beginners)

SQLite is perfect for learning dbt as it doesn't require server configuration:

```bash
# Install SQLite (if not installed)
# macOS
brew install sqlite

# Ubuntu/Debian
sudo apt install sqlite3
```

### PostgreSQL (Production)

```bash
# Install PostgreSQL
# macOS
brew install postgresql

# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib

# Start service
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

## 📁 Project Structure

After installation, you'll have a structure like this:

```
dbt_course/
├── dbt_project.yml          # Main configuration
├── profiles.yml             # Connection configurations
├── models/                  # SQL models
│   ├── staging/            # Staging models
│   ├── marts/              # Mart models
│   └── analytics/          # Analytical models
├── tests/                   # Custom tests
├── macros/                  # Reusable macros
├── seeds/                   # Static data
└── docs/                    # Documentation
```

## 🔐 Profile Configuration

Create the file `~/.dbt/profiles.yml`:

```yaml
# For SQLite
jaffle_shop:
  target: dev
  outputs:
    dev:
      type: sqlite
      path: "{{ env_var('DBT_SQLITE_PATH', '/tmp/jaffle_shop.db') }}"
      threads: 1

# For PostgreSQL
jaffle_shop:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      user: "{{ env_var('DBT_USER') }}"
      password: "{{ env_var('DBT_PASS') }}"
      port: 5432
      dbname: jaffle_shop
      schema: public
      threads: 4
```

## 🚀 First Project

Now you're ready to create your first dbt project! Go to the next section:

[**Project Setup**](../jaffle-shop/project-setup.md)

## 🔍 Installation Verification

Run these commands to verify everything is working:

```bash
# Check dbt version
dbt --version

# Check if adapter is installed
dbt debug

# Create test project
dbt init test_project
cd test_project
dbt run
```

## 🆘 Troubleshooting

### Error: "dbt command not found"
- Check if virtual environment is activated
- Verify dbt was installed correctly

### Database Connection Error
- Check configurations in `profiles.yml`
- Test connection manually
- Verify database is running

### Dependency Error
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 📚 Next Steps

1. ✅ **Environment configured** ← You are here
2. [Setup Project](../jaffle-shop/project-setup.md)
3. [Explore Jaffle Shop](../jaffle-shop/overview.md)

---

**Is your environment configured?** 🎯

Let's go to the next step: [project setup](../jaffle-shop/project-setup.md)!
