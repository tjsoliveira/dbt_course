#!/bin/bash

# Script to initialize the dbt project
# Checks if profiles.yml exists in the dbt project root

# Path to the dbt project directory (jaffle_shop)
DBT_PROJECT_DIR="jaffle_shop"

# Generate custom data using jafgen
echo ""
echo "Generating custom data using jafgen..."

# Check if jafgen is available
if ! command -v jafgen &> /dev/null; then
    echo "Error: jafgen not found! Make sure it's installed in the virtual environment."
    exit 1
fi

# Create seeds directory if it doesn't exist
SEEDS_DIR="$DBT_PROJECT_DIR/seeds"
mkdir -p "$SEEDS_DIR"

# Navigate to the seeds directory to generate files
cd "$SEEDS_DIR"

echo "Running jafgen to generate data..."
jafgen 2

echo ""
echo "🎉 dbt project initialized with custom data!"
echo "To load data into the database, run:"
echo "  cd $DBT_PROJECT_DIR"
echo "  dbt seed"
