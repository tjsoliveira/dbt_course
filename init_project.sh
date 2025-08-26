#!/bin/bash

# Script to initialize the dbt project
# Generates custom data using Python scripts and runs dbt seed

# Path to the dbt project directory (jaffle_shop)
DBT_PROJECT_DIR="jaffle_shop"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}🚀 Initializing dbt project with custom data...${NC}"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python3 not found! Make sure it's installed.${NC}"
    exit 1
fi

# Check if required Python packages are installed
echo -e "${YELLOW}Checking Python dependencies...${NC}"
python3 -c "import faker" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Faker package not found! Installing dependencies...${NC}"
    pip install -r requirements.txt
fi

# Create seeds directory if it doesn't exist
SEEDS_DIR="$DBT_PROJECT_DIR/seeds/jaffle-data"
mkdir -p "$SEEDS_DIR"

echo ""
echo -e "${YELLOW}📊 Generating all data using centralized script...${NC}"
python3 scripts/generate_all_data.py

# Check if data generation was successful
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Data generation failed! Check the output above.${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ All data generated successfully!${NC}"
echo ""

# Navigate to dbt project directory
cd "$DBT_PROJECT_DIR"

echo -e "${YELLOW}🌱 Running dbt seed to load data into database...${NC}"
dbt seed -f

echo ""
echo -e "${GREEN}🎉 dbt project initialized with custom data!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "  - Run models: dbt run"
echo "  - Run tests: dbt test"
echo "  - Generate docs: dbt docs generate"
echo ""
