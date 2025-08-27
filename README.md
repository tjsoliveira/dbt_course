# 🚀 dbt Course - Practical Data Transformation

[![GitHub Pages](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://tjsoliveira.github.io/dbt_course/)
[![dbt](https://img.shields.io/badge/dbt-Core-orange)](https://www.getdbt.com/)
[![SQLite](https://img.shields.io/badge/database-SQLite-blue)](https://www.sqlite.org/)
[![Python](https://img.shields.io/badge/python-3.8+-green)](https://www.python.org/)

A comprehensive, practical dbt (data build tool) course inspired by **Jaffle Shop** project. 
Learn data transformation, testing, and documentation with real-world examples and best practices.

## 📖 **Course Documentation**

🌐 **[Access the full course documentation →](https://tjsoliveira.github.io/dbt_course/)**

The complete course materials, tutorials, and guides are available on our GitHub Pages site with:
- 📚 Interactive documentation with search
- 🎯 Step-by-step tutorials  
- 💡 Best practices and real examples
- 🔧 Setup guides for all operating systems
- 📊 Data generation tools and scripts

## 🎯 **What You'll Learn**

- ✅ **dbt Fundamentals**: Installation, configuration, and core concepts
- ✅ **Data Modeling**: Staging, marts, and analytical models
- ✅ **Data Quality**: Comprehensive testing strategies
- ✅ **Documentation**: Auto-generated and rich documentation
- ✅ **Best Practices**: Industry standards and maintainable code
- ✅ **Real Project**: Based on Jaffle Shop e-commerce project

## 🏪 **About the Project**

This project is a fictional online store that sells various products. This realistic dataset includes:

- **👥 Customers**: Demographics, contact info, and behavior data
- **🛍️ Products**: Complete catalog with categories and brands  
- **📦 Orders**: Transaction history and order details
- **📊 Analytics**: Business metrics and KPI calculations

Perfect for learning data transformations in a business context!

## 🚀 **Quick Start**

### Option 1: Automated Setup (Recommended)
```bash
# Clone the repository
git clone https://github.com/tjsoliveira/dbt_course.git
cd dbt_course

# Run the setup script
./init_project.sh
```

### Option 2: Manual Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate sample data
cd jaffle_shop
python scripts/generate_all_data.py

# Run dbt
dbt run
dbt test
```

## 📁 **Project Structure**

```
dbt_course/
├── 📚 docs/                     # Course documentation (GitHub Pages)
├── 🏪 jaffle_shop/             # Main dbt project
│   ├── models/                 # SQL transformation models
│   │   ├── staging/           # Raw data cleaning
│   │   ├── marts/             # Business logic
│   │   └── analytics/         # Final analytics
│   ├── tests/                  # Data quality tests
│   ├── macros/                 # Reusable SQL code
│   ├── seeds/                  # Static reference data
│   └── scripts/                # Data generation utilities
├── 🔧 requirements.txt         # Python dependencies
├── 📖 README.md               # This file
└── 🚀 init_project.sh         # Automated setup script
```

## 📊 **Sample Data Generation**

Generate realistic sample data with intentional quality issues for testing:

```bash
cd jaffle_shop

# Generate all data at once (recommended)
python scripts/generate_all_data.py

# Or generate specific datasets
python scripts/generate_customer_data.py
python scripts/generate_products_data.py
python scripts/generate_items_data.py
```

**Features:**
- 🇧🇷 **Brazilian data**: Realistic names, addresses, and phone numbers
- 🐛 **Quality issues**: Intentional data problems to test your models
- 📈 **Scalable**: Generate from hundreds to thousands of records
- 🔄 **Relationships**: Proper foreign key relationships between tables

## 🧪 **Running the Course**

```bash
cd jaffle_shop

# Build all models
dbt build

# Generate documentation
dbt docs generate
dbt docs serve
```

## 📚 **Course Sections**

| Section | Description | Status |
|---------|-------------|--------|
| [🔰 Introduction](https://tjsoliveira.github.io/dbt_course/intro/what-is-dbt/) | What is dbt and why use it | ✅ |
| [⚙️ Setup](https://tjsoliveira.github.io/dbt_course/intro/setup/) | Environment configuration | ✅ |
| [🏪 Project](https://tjsoliveira.github.io/dbt_course/jaffle-shop/overview/) | Project overview and setup | ✅ |
| [📊 Sources](https://tjsoliveira.github.io/dbt_course/course/sources/) | Working with source data | ✅ |
| [🔄 Models](https://tjsoliveira.github.io/dbt_course/course/models/) | Building transformation models | ✅ |
| [✅ Tests](https://tjsoliveira.github.io/dbt_course/course/tests/) | Data quality and testing | ✅ |
| [📚 Documentation](https://tjsoliveira.github.io/dbt_course/course/documentation/) | Project documentation with YAML, Markdown, and interactive docs | ✅ |
## 🛠️ **Technologies Used**

- **[dbt Core](https://www.getdbt.com/)** - Data transformation tool
- **[SQLite](https://www.sqlite.org/)** - Lightweight database (perfect for learning)
- **[Python](https://www.python.org/)** - Data generation and automation
- **[Faker](https://faker.readthedocs.io/)** - Realistic sample data generation
- **[MkDocs Material](https://squidfunk.github.io/mkdocs-material/)** - Beautiful documentation

## 🤝 **Contributing**

Contributions are welcome! Here's how you can help:

- 🐛 **Report bugs** or suggest improvements
- 📖 **Improve documentation** or add examples
- 🔧 **Add new features** or enhance existing ones
- 💡 **Share ideas** for course improvements

### Development Setup
```bash
# Fork and clone the repository
git clone https://github.com/your-username/dbt_course.git

# Set up development environment
./init_project.sh
```

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 **About the Author**

This course was created by **Thiago Oliveira**, a Senior Data Engineer and Analytics Engineer with 10+ years of experience in data and technology. Currently working at Arco Educação, Thiago is a dbt Certified Developer who has implemented data transformation pipelines in production environments using dbt, Airflow, Snowflake, and AWS.

With a Master's degree in Databases and extensive experience at companies like ZENVIA and ENAP, Thiago brings real-world expertise to help you master dbt and modern data engineering practices.

🔗 [Learn more about the author](https://tjsoliveira.github.io/dbt_course/about-author/)
## 🌟 **Acknowledgments**

- **[dbt Labs](https://www.getdbt.com/)** for creating the amazing dbt tool
- **[Jaffle Shop](https://github.com/dbt-labs/jaffle_shop)** original project inspiration
- **dbt Community** for best practices and examples

## 📞 **Support ## 📞 **Support** Contact**

- 📖 **Documentation**: [https://tjsoliveira.github.io/dbt_course/](https://tjsoliveira.github.io/dbt_course/)
- 🐛 **Issues**: [GitHub Issues](https://github.com/tjsoliveira/dbt_course/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/tjsoliveira/dbt_course/discussions)
- 👔 **LinkedIn**: [Thiago Oliveira](https://www.linkedin.com/in/tjsoliveira/)
---

**Ready to start your dbt journey?** 🚀

[**📖 Go to Course Documentation →**](https://tjsoliveira.github.io/dbt_course/)
