#!/usr/bin/env python3
"""
Script to generate CSV data for items and orders using Faker
Generates data that corresponds to the columns of the stg_items.sql and stg_orders.sql models
"""

import csv
import random
import os
from datetime import datetime, timedelta
from faker import Faker
import argparse
from config import (
    ITEMS_FILE, ORDERS_FILE, DEFAULT_NUM_ITEMS, DEFAULT_NUM_ORDERS,
    PROBLEM_PERCENTAGES, ORDER_PROBLEM_TYPES, VALUE_RANGES,
    ORDER_STATUSES, PAYMENT_METHODS, DATE_RANGES
)

# Configure Faker for Brazilian Portuguese
fake = Faker(['pt_BR'])

def generate_problematic_order(order_date, status, problem_type):
    """Generates problematic order data based on problem type from configuration"""
    if problem_type == 'negative_amount':
        total_amount = round(random.uniform(*VALUE_RANGES['negative_amount']), 2)
        return order_date, status, total_amount
    elif problem_type == 'zero_amount':
        return order_date, status, 0
    elif problem_type == 'missing_date':
        return None, status, 0
    elif problem_type == 'missing_status':
        return order_date, None, 0
    elif problem_type == 'suspiciously_high':
        total_amount = round(random.uniform(*VALUE_RANGES['suspiciously_high']), 2)
        return order_date, status, total_amount
    elif problem_type == 'future_date':
        # Future date (between 1 and 30 days in the future)
        future_date = datetime.now().date() + timedelta(days=random.randint(*VALUE_RANGES['future_date_days']))
        return future_date, status, 0
    else:
        return order_date, status, 0  # Default fallback

def generate_items_data(num_records=DEFAULT_NUM_ITEMS, num_orders=DEFAULT_NUM_ORDERS):
    """Generates items and orders data"""
    
    # Generate orders first
    orders = []
    for i in range(num_orders):
        # Creation date between configured range
        created_at = fake.date_between_dates(
            date_start=datetime.fromisoformat(DATE_RANGES['orders']['start']).date()
        )
        
        # Random status
        status = random.choice(ORDER_STATUSES)
        
        # Random payment method
        payment_method = random.choice(PAYMENT_METHODS)
        
        # Delivery address
        delivery_address = fake.street_address()
        
        # Generate data problems to test problematic_orders
        order_date = created_at
        total_amount = 0  # Will be calculated based on items
        
        # Use configured percentage for orders with data problems
        if i < int(num_orders * PROBLEM_PERCENTAGES['orders']['data_problems']):
            # Randomly select problem type
            problem_type = random.choice(ORDER_PROBLEM_TYPES)
            order_date, status, total_amount = generate_problematic_order(order_date, status, problem_type)
        
        order = {
            'id': i + 1,
            'customer_id': random.randint(1, 1000),  # Assuming 1000 customers
            'order_date': order_date.strftime('%Y-%m-%d') if order_date else None,
            'status': status,
            'total_amount': total_amount,  # Will be calculated based on items if not a problem
            'payment_method': payment_method,
            'delivery_address': delivery_address,
            'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        orders.append(order)
    
    # Generate items
    items = []
    item_id = 1
    
    for order in orders:
        # If order doesn't have value problem, calculate based on items
        if order['total_amount'] == 0 and order['order_date'] is not None:
            # Each order will have between 1 and 5 items
            num_items_in_order = random.randint(1, 5)
            
            for _ in range(num_items_in_order):
                # Generate item data
                quantity = random.randint(1, 10)
                unit_price = round(random.uniform(10.0, 500.0), 2)
                
                # Calculate item total
                total_price = quantity * unit_price
                
                # Add to order total
                order['total_amount'] += total_price
                
                item = {
                    'item_id': item_id,
                    'order_id': order['id'],
                    'product_id': random.randint(1, 1000),  # Fictitious product IDs
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'created_at': order['created_at']
                }
                
                items.append(item)
                item_id += 1
        else:
            # For problematic orders, create at least one item to maintain referential integrity
            # but don't calculate total (already defined by problem)
            item = {
                'item_id': item_id,
                'order_id': order['id'],
                'product_id': random.randint(1, 1000),
                'quantity': random.randint(1, 5),
                'unit_price': round(random.uniform(10.0, 100.0), 2),
                'created_at': order['created_at']
            }
            
            items.append(item)
            item_id += 1
    
    return items, orders

def save_to_csv(data, filename, fieldnames):
    """Saves data to CSV file"""
    
    if not data:
        print("No data to save!")
        return
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write data
            for row in data:
                writer.writerow(row)
        
        print(f"Data saved to {filename}")
        print(f"Total records: {len(data)}")
        
    except Exception as e:
        print(f"Error saving {filename}: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(
        description='Generate CSV data for items and orders using Faker'
    )
    parser.add_argument(
        '-n', '--num-items',
        type=int,
        default=DEFAULT_NUM_ITEMS,
        help=f'Number of items to generate (default: {DEFAULT_NUM_ITEMS})'
    )
    parser.add_argument(
        '-o', '--num-orders',
        type=int,
        default=DEFAULT_NUM_ORDERS,
        help=f'Number of orders to generate (default: {DEFAULT_NUM_ORDERS})'
    )

    
    args = parser.parse_args()
    
    print(f"Generating {args.num_orders} orders with {args.num_items} items...")
    
    # Generate data
    items, orders = generate_items_data(args.num_items, args.num_orders)
    
    # Save items
    items_fieldnames = ['item_id', 'order_id', 'product_id', 'quantity', 'unit_price', 'created_at']
    save_to_csv(items, ITEMS_FILE, items_fieldnames)
    
    # Save orders
    orders_fieldnames = ['id', 'customer_id', 'order_date', 'status', 'total_amount', 'payment_method', 'delivery_address', 'created_at']
    save_to_csv(orders, ORDERS_FILE, orders_fieldnames)
    
    # Show example of first records
    print("\n=== Example of first 3 items ===")
    for i, item in enumerate(items[:3]):
        print(f"\nItem {i+1}:")
        for key, value in item.items():
            print(f"  {key}: {value}")
    
    print("\n=== Example of first 3 orders ===")
    for i, order in enumerate(orders[:3]):
        print(f"\nOrder {i+1}:")
        for key, value in order.items():
            print(f"  {key}: {value}")

if __name__ == "__main__":
    main()
