#!/usr/bin/env python3
"""
Script to generate CSV data for products using Faker
Generates data that corresponds to the columns of the stg_products.sql model
"""

import csv
import random
import os
from datetime import datetime
from faker import Faker
import argparse
from config import (
    PRODUCTS_FILE, DEFAULT_NUM_PRODUCTS, PROBLEM_PERCENTAGES,
    DATE_RANGES, PRODUCT_CATEGORIES, PRODUCTS_BY_CATEGORY,
    PRODUCT_PROBLEM_TYPES, VALUE_RANGES
)

# Configure Faker for Brazilian Portuguese
fake = Faker(['pt_BR'])

def generate_problematic_price(problem_type):
    """Generates problematic price based on problem type from configuration"""
    if problem_type == 'negative_price':
        return round(random.uniform(*VALUE_RANGES['negative_price']), 2)
    elif problem_type == 'zero_price':
        return 0
    elif problem_type == 'extremely_high_price':
        return round(random.uniform(*VALUE_RANGES['extremely_high_price']), 2)
    elif problem_type == 'missing_price':
        return None
    else:
        return round(random.uniform(10.0, 1000.0), 2)  # Default fallback

def generate_product_data(num_records=DEFAULT_NUM_PRODUCTS):
    """Generates product data"""
    
    products = []
    
    for i in range(num_records):
        # Select category randomly
        category = random.choice(PRODUCT_CATEGORIES)
        
        # Select product from category or generate generic one
        if category in PRODUCTS_BY_CATEGORY and PRODUCTS_BY_CATEGORY[category]:
            product_name = random.choice(PRODUCTS_BY_CATEGORY[category])
        else:
            product_name = f"Generic {category} Product {i+1}"
        
        # Generate price (some products will have price problems)
        if random.random() < PROBLEM_PERCENTAGES['products']['price_problems']:
            price_problem = random.choice(PRODUCT_PROBLEM_TYPES)
            price = generate_problematic_price(price_problem)
        else:
            # Normal prices
            price = round(random.uniform(10.0, 1000.0), 2)
        
        # Creation date
        created_at = fake.date_between_dates(
            date_start=datetime.fromisoformat(DATE_RANGES['products']['start']).date()
        )
        
        # Update date
        updated_at = fake.date_between_dates(
            date_start=created_at
        )
        
        product = {
            'id': i + 1,
            'name': product_name,
            'category': category,
            'price': price,
            'description': fake.text(max_nb_chars=200),
            'brand': fake.company(),
            'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        products.append(product)
    
    return products

def save_to_csv(products, filename=PRODUCTS_FILE):
    """Saves data to CSV file"""
    
    if not products:
        print("No data to save!")
        return
    
    # Get columns from first record
    fieldnames = list(products[0].keys())
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Write data
        for product in products:
            writer.writerow(product)
    
    print(f"Data saved to {filename}")
    print(f"Total records: {len(products)}")

def main():
    parser = argparse.ArgumentParser(
        description='Generate CSV data for products using Faker'
    )
    parser.add_argument(
        '-n', '--num-products',
        type=int,
        default=DEFAULT_NUM_PRODUCTS,
        help=f'Number of products to generate (default: {DEFAULT_NUM_PRODUCTS})'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=PRODUCTS_FILE,
        help=f'Output filename (default: {PRODUCTS_FILE})'
    )
    
    args = parser.parse_args()
    
    print(f"Generating {args.num_products} products...")
    
    # Generate data
    products = generate_product_data(args.num_products)
    
    # Save to CSV
    save_to_csv(products, args.output)
    
    # Show example of first records
    print("\n=== Example of first 5 products ===")
    for i, product in enumerate(products[:5]):
        print(f"\nProduct {i+1}:")
        for key, value in product.items():
            print(f"  {key}: {value}")
    
    # Show statistics
    print("\n=== Statistics ===")
    category_counts = {}
    for product in products:
        category = product['category']
        category_counts[category] = category_counts.get(category, 0) + 1
    
    print("Products by category:")
    for category, count in sorted(category_counts.items()):
        print(f"  {category}: {count} products")

if __name__ == "__main__":
    main()
