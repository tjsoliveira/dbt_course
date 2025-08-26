#!/usr/bin/env python3
"""
Script to generate CSV data for customers using Faker
Generates data that corresponds to the columns of the stg_customers.sql model
Includes intentional duplicates for testing duplicate detection
"""

import csv
import random
from datetime import datetime, timedelta
from faker import Faker
import argparse
from config import (
    CUSTOMERS_FILE, DEFAULT_NUM_CUSTOMERS, PROBLEM_PERCENTAGES,
    DATE_RANGES, BRAZILIAN_DATA, INVALID_DATA_EXAMPLES
)

# Configure Faker for Brazilian Portuguese
fake = Faker(['pt_BR'])

def generate_phone():
    """Generates a valid Brazilian phone number"""
    # Formats: (11) 99999-9999 or 11999999999
    ddd = random.randint(11, 99)
    phone = random.randint(100000000, 999999999)
    return f"({ddd}) {phone//10000}-{phone%10000}"

def generate_zip_code():
    """Generates a valid Brazilian ZIP code"""
    return f"{random.randint(10000, 99999)}-{random.randint(100, 999)}"

def generate_invalid_email(first_name, last_name, problem_type):
    """Generates invalid email based on problem type from configuration"""
    if problem_type == 'no_at_symbol':
        return f"{first_name.lower()}.{last_name.lower()}"
    elif problem_type == 'no_domain':
        return f"{first_name.lower()}@{last_name.lower()}"
    elif problem_type == 'no_username':
        return f"@{first_name.lower()}.{last_name.lower()}"
    elif problem_type == 'incomplete_domain':
        return f"{first_name.lower()}.{last_name.lower()}@"
    elif problem_type == 'no_at_with_domain':
        return f"{first_name.lower()}.{last_name.lower()}.com"
    elif problem_type == 'empty_string':
        return ""
    elif problem_type == 'null_value':
        return None
    else:
        return f"{first_name.lower()}.{last_name.lower()}"  # Default fallback

def generate_invalid_phone(problem_type):
    """Generates invalid phone based on problem type from configuration"""
    if problem_type == 'too_short':
        return "123"
    elif problem_type == 'too_long':
        return "12345678901234567890"
    elif problem_type == 'with_letters':
        return "abc-def-ghij"
    elif problem_type == 'incorrect_format1':
        return "(11) 1234-567"
    elif problem_type == 'incorrect_format2':
        return "11 12345 6789"
    elif problem_type == 'empty_string':
        return ""
    elif problem_type == 'null_value':
        return None
    elif problem_type == 'only_zeros':
        return "000000000"
    elif problem_type == 'only_nines':
        return "999999999"
    elif problem_type == 'wrong_format':
        return "123-456-789"
    else:
        return "123"  # Default fallback

def create_duplicate_variations(base_customer, duplicate_type):
    """Creates variations of a customer that could be considered duplicates"""
    
    if duplicate_type == 'name_variation':
        # Same name, different email/phone
        return {
            'id': base_customer['id'] + 10000,  # Different ID
            'first_name': base_customer['first_name'],
            'last_name': base_customer['last_name'],
            'email': f"{base_customer['first_name'].lower()}.{base_customer['last_name'].lower()}2@{fake.free_email_domain()}",
            'phone': generate_phone(),
            'address': fake.street_address(),
            'city': base_customer['city'],
            'state': base_customer['state'],
            'zip_code': generate_zip_code(),
            'created_at': base_customer['created_at'],
            'updated_at': base_customer['updated_at']
        }
    
    elif duplicate_type == 'email_variation':
        # Same email, different name/phone
        return {
            'id': base_customer['id'] + 20000,  # Different ID
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': base_customer['email'],
            'phone': generate_phone(),
            'address': fake.street_address(),
            'city': random.choice(BRAZILIAN_DATA['cities']),
            'state': random.choice(BRAZILIAN_DATA['states']),
            'zip_code': generate_zip_code(),
            'created_at': base_customer['created_at'],
            'updated_at': base_customer['updated_at']
        }
    
    elif duplicate_type == 'phone_variation':
        # Same phone, different name/email
        return {
            'id': base_customer['id'] + 30000,  # Different ID
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': f"{fake.first_name().lower()}.{fake.last_name().lower()}@{fake.free_email_domain()}",
            'phone': base_customer['phone'],
            'address': fake.street_address(),
            'city': random.choice(BRAZILIAN_DATA['cities']),
            'state': random.choice(BRAZILIAN_DATA['states']),
            'zip_code': generate_zip_code(),
            'created_at': base_customer['created_at'],
            'updated_at': base_customer['updated_at']
        }
    
    elif duplicate_type == 'similar_name':
        # Similar names (typos, abbreviations)
        first_name_variations = [
            base_customer['first_name'],
            base_customer['first_name'][:3] + '.',  # Abbreviation
            base_customer['first_name'].replace('a', 'o').replace('e', 'i'),  # Similar letters
            base_customer['first_name'] + 'a',  # Extra letter
            base_customer['first_name'][:-1] if len(base_customer['first_name']) > 1 else base_customer['first_name']  # Missing letter
        ]
        
        last_name_variations = [
            base_customer['last_name'],
            base_customer['last_name'][:3] + '.',  # Abbreviation
            base_customer['last_name'].replace('a', 'o').replace('e', 'i'),  # Similar letters
            base_customer['last_name'] + 'a',  # Extra letter
            base_customer['last_name'][:-1] if len(base_customer['last_name']) > 1 else base_customer['last_name']  # Missing letter
        ]
        
        return {
            'id': base_customer['id'] + 40000,  # Different ID
            'first_name': random.choice(first_name_variations),
            'last_name': random.choice(last_name_variations),
            'email': f"{fake.first_name().lower()}.{fake.last_name().lower()}@{fake.free_email_domain()}",
            'phone': generate_phone(),
            'address': fake.street_address(),
            'city': base_customer['city'],
            'state': base_customer['state'],
            'zip_code': generate_zip_code(),
            'created_at': base_customer['created_at'],
            'updated_at': base_customer['updated_at']
        }
    
    else:
        return None

def generate_customer_data(num_records=DEFAULT_NUM_CUSTOMERS):
    """Generates customer data with intentional duplicates"""
    
    customers = []
    base_customers = []
    
    # First, generate base customers
    for i in range(num_records):
        # Creation date between configured range
        created_at = fake.date_between_dates(
            date_start=datetime.fromisoformat(DATE_RANGES['customers']['start']).date()
        )
        
        # Update date (can be equal to or after creation)
        updated_at = fake.date_between_dates(
            date_start=created_at
        )
        
        # Generate email (some valid, others invalid)
        first_name = fake.first_name()
        last_name = fake.last_name()
        
        # Use configured percentage for invalid emails
        if random.random() < PROBLEM_PERCENTAGES['customers']['invalid_email']:
            # Select random problem type from configuration
            problem_type = random.choice(INVALID_DATA_EXAMPLES['emails'])
            email = generate_invalid_email(first_name, last_name, problem_type)
        else:
            # Valid emails
            email = f"{first_name.lower()}.{last_name.lower()}@{fake.free_email_domain()}"
        
        # Generate phone (some valid, others invalid)
        phone = None
        if random.random() > PROBLEM_PERCENTAGES['customers']['no_phone']:
            if random.random() < PROBLEM_PERCENTAGES['customers']['invalid_phone']:
                # Select random problem type from configuration
                problem_type = random.choice(INVALID_DATA_EXAMPLES['phones'])
                phone = generate_invalid_phone(problem_type)
            else:
                phone = generate_phone()
        
        customer = {
            'id': i + 1,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'address': fake.street_address(),
            'city': random.choice(BRAZILIAN_DATA['cities']),
            'state': random.choice(BRAZILIAN_DATA['states']),
            'zip_code': generate_zip_code(),
            'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        customers.append(customer)
        base_customers.append(customer)
    
    # Now add intentional duplicates (about 3% of base customers will have duplicates)
    duplicate_types = ['name_variation', 'email_variation', 'phone_variation', 'similar_name']
    
    for base_customer in base_customers:
        # 3% chance to create duplicates
        if random.random() < 0.03:
            # Select random duplicate type
            duplicate_type = random.choice(duplicate_types)
            duplicate = create_duplicate_variations(base_customer, duplicate_type)
            
            if duplicate:
                customers.append(duplicate)
                
                # 30% chance to create a second duplicate (triplicate)
                if random.random() < 0.30:
                    duplicate2 = create_duplicate_variations(base_customer, random.choice(duplicate_types))
                    if duplicate2:
                        customers.append(duplicate2)
    
    return customers

def save_to_csv(customers, filename=CUSTOMERS_FILE, num_records=None):
    """Saves data to CSV file"""
    
    if not customers:
        print("No data to save!")
        return
    
    # Get columns from first record
    fieldnames = list(customers[0].keys())
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Write data
        for customer in customers:
            writer.writerow(customer)
    
    print(f"Data saved to {filename}")
    print(f"Total records: {len(customers)}")
    
    # Count duplicates for reporting
    if num_records:
        duplicate_count = len(customers) - num_records
        print(f"Base customers: {num_records}")
        print(f"Duplicate records added: {duplicate_count}")

def main():
    parser = argparse.ArgumentParser(
        description='Generate CSV data for customers using Faker'
    )
    parser.add_argument(
        '-n', '--num-records',
        type=int,
        default=DEFAULT_NUM_CUSTOMERS,
        help=f'Number of records to generate (default: {DEFAULT_NUM_CUSTOMERS})'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=CUSTOMERS_FILE,
        help=f'Output filename (default: {CUSTOMERS_FILE})'
    )
    
    args = parser.parse_args()
    
    print(f"Generating {args.num_records} customer records...")
    
    # Generate data
    customers = generate_customer_data(args.num_records)
    
    # Save to CSV
    save_to_csv(customers, args.output, args.num_records)
    
    # Show example of first records
    print("\nExample of first 3 records:")
    for i, customer in enumerate(customers[:3]):
        print(f"\nRecord {i+1}:")
        for key, value in customer.items():
            print(f"  {key}: {value}")

if __name__ == "__main__":
    main()
