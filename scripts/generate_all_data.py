#!/usr/bin/env python3
"""
Main script to generate all CSV data using individual scripts
Generates data that includes problems to test the problematic_orders model
"""

import subprocess
import sys
import os
from config import (
    DEFAULT_NUM_CUSTOMERS, DEFAULT_NUM_PRODUCTS, 
    DEFAULT_NUM_ORDERS, DEFAULT_NUM_ITEMS
)

def run_script(script_name, args=None):
    """Executes a Python script and returns the result"""
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    
    if args is None:
        args = []
    
    cmd = [sys.executable, script_path] + args
    
    print(f"\n{'='*50}")
    print(f"Executing: {script_name}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ Success!")
        if result.stdout:
            print("Output:")
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Execution error!")
        print(f"Exit code: {e.returncode}")
        if e.stdout:
            print("Standard output:")
            print(e.stdout)
        if e.stderr:
            print("Error:")
            print(e.stderr)
        return False

def main():
    """Main function that executes all scripts"""
    
    print("🚀 Starting generation of all data...")
    print("This script will generate data with problems to test problematic_orders")
    
    # Configuration to generate data with problems using constants
    config = {
        'customers': ['-n', str(DEFAULT_NUM_CUSTOMERS)],  # Use constant for customers
        'products': ['-n', str(DEFAULT_NUM_PRODUCTS)],    # Use constant for products
        'orders': ['-n', str(DEFAULT_NUM_ITEMS), '-o', str(DEFAULT_NUM_ORDERS)]  # Use constants for orders
    }
    
    # Execute scripts in sequence
    scripts_to_run = [
        ('generate_customer_data.py', config['customers']),
        ('generate_products_data.py', config['products']),
        ('generate_items_data.py', config['orders'])
    ]
    
    success_count = 0
    total_scripts = len(scripts_to_run)
    
    for script_name, args in scripts_to_run:
        if run_script(script_name, args):
            success_count += 1
        else:
            print(f"⚠️  Failed to execute {script_name}")
    
    # Final summary
    print(f"\n{'='*50}")
    print("📊 EXECUTION SUMMARY")
    print(f"{'='*50}")
    print(f"Scripts executed successfully: {success_count}/{total_scripts}")
    
    if success_count == total_scripts:
        print("🎉 All data was generated successfully!")
        print("\n📁 Generated files:")
        print("  - seeds/jaffle-data/raw_customers.csv")
        print("  - seeds/jaffle-data/raw_products.csv")
        print("  - seeds/jaffle-data/raw_orders.csv")
        print("  - seeds/jaffle-data/raw_items.csv")
        print("\n🔍 Data includes problems to test:")
        print("  - Orders with negative, zero or very high values")
        print("  - Orders with future or missing dates")
        print("  - Orders with missing status")
        print("  - Customers with invalid emails and phones")
        print("  - Products with negative, zero or very high prices")
        print(f"\n📊 Generated quantities:")
        print(f"  - Customers: {DEFAULT_NUM_CUSTOMERS}")
        print(f"  - Products: {DEFAULT_NUM_PRODUCTS}")
        print(f"  - Orders: {DEFAULT_NUM_ORDERS}")
        print(f"  - Items: {DEFAULT_NUM_ITEMS}")
    else:
        print("❌ Some scripts failed. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
