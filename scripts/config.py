#!/usr/bin/env python3
"""
Configuration file for data generation scripts
Centralizes all file paths and configuration constants
"""

import os

# Project root directory (relative to scripts directory)
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')

# Seeds directory path
SEEDS_DIR = os.path.join(PROJECT_ROOT, 'jaffle_shop', 'seeds', 'jaffle-data')

# Output file paths
CUSTOMERS_FILE = os.path.join(SEEDS_DIR, 'raw_customers.csv')
PRODUCTS_FILE = os.path.join(SEEDS_DIR, 'products.csv')
ORDERS_FILE = os.path.join(SEEDS_DIR, 'raw_orders.csv')
ITEMS_FILE = os.path.join(SEEDS_DIR, 'raw_items.csv')

# Data generation defaults
DEFAULT_NUM_CUSTOMERS = 3000
DEFAULT_NUM_PRODUCTS = 1000
DEFAULT_NUM_ORDERS = 10000
DEFAULT_NUM_ITEMS = 20000

# Data quality problem percentages
PROBLEM_PERCENTAGES = {
    'customers': {
        'invalid_email': 0.05,  # 5% of customers have invalid emails
        'invalid_phone': 0.10,  # 10% of customers have invalid phones
        'no_phone': 0.01       # 1% of customers have no phone
    },
    'products': {
        'price_problems': 0.05,  # 5% of products have price problems
        'stock_problems': 0.05   # 5% of products have stock problems
    },
    'orders': {
        'data_problems': 0.02    # 2% of orders have data problems
    }
}

# Problem types for orders
ORDER_PROBLEM_TYPES = [
    'negative_amount',
    'zero_amount', 
    'missing_date',
    'missing_status',
    'suspiciously_high',
    'future_date'
]

# Problem types for products
PRODUCT_PROBLEM_TYPES = [
    'negative_price',
    'zero_price',
    'extremely_high_price',
    'missing_price'
]

# Date ranges
DATE_RANGES = {
    'customers': {
        'start': '2024-01-01',
        'end': '2025-12-31'
    },
    'products': {
        'start': '2020-01-01',
        'end': '2025-12-31'
    },
    'orders': {
        'start': '2024-01-01',
        'end': '2025-12-31'
    }
}

# Value ranges for problems
VALUE_RANGES = {
    'negative_amount': (-1000.0, -1.0),
    'suspiciously_high': (10001.0, 50000.0),
    'negative_price': (-100.0, -1.0),
    'extremely_high_price': (100000.0, 1000000.0),
    'future_date_days': (1, 30)
}

# Brazilian geographic data
BRAZILIAN_DATA = {
    'states': [
        'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
        'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
        'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
    ],
    'cities': [
        'São Paulo', 'Rio de Janeiro', 'Brasília', 'Salvador', 'Fortaleza',
        'Belo Horizonte', 'Manaus', 'Curitiba', 'Recife', 'Porto Alegre',
        'Goiânia', 'Belém', 'Guarulhos', 'Campinas', 'São Luís',
        'São Gonçalo', 'Maceió', 'Duque de Caxias', 'Natal', 'Teresina'
    ]
}

# Product categories and data
PRODUCT_CATEGORIES = [
    'Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports',
    'Beauty', 'Food', 'Toys', 'Automotive', 'Health'
]

PRODUCTS_BY_CATEGORY = {
    'Electronics': [
        'Galaxy S23 Smartphone', 'Dell Inspiron Laptop', 'Bluetooth Headphones',
        '55" Smart TV', 'iPad Tablet', 'Canon Digital Camera', 'PlayStation 5 Console'
    ],
    'Clothing': [
        'Basic T-Shirt', 'Denim Jeans', 'Casual Dress', 'Leather Jacket',
        'Sports Sneakers', 'Social Blazer', 'Summer Shorts'
    ],
    'Books': [
        'The Lord of the Rings', 'Harry Potter', 'The Great Gatsby', '1984',
        'To Kill a Mockingbird', 'Pride and Prejudice', 'The Catcher in the Rye'
    ],
    'Home & Garden': [
        'Decorative Vase', 'Table Lamp', 'Cookware Set', 'Dining Table',
        '3-Seater Sofa', 'Persian Rug', 'Abstract Painting'
    ],
    'Sports': [
        'Soccer Ball', 'Tennis Racket', 'Mountain Bike',
        'Surfboard', 'Gym Weights', 'Running Shoes'
    ]
}

# Order statuses and payment methods
ORDER_STATUSES = [
    'pending', 'processing', 'shipped', 'delivered', 'cancelled', 'returned'
]

PAYMENT_METHODS = [
    'credit_card', 'debit_card', 'pix', 'boleto', 'paypal', 'cash'
]

# Invalid data examples for testing
INVALID_DATA_EXAMPLES = {
    'emails': [
        'no_at_symbol',
        'no_domain',
        'empty_string',
        'null_value'
    ],
    'phones': [
        'too_short',
        'too_long',
        'with_letters',
        'empty_string',
        'null_value'
    ]
}
