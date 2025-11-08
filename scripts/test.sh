#!/bin/bash

# BLKSHP OS Testing Script
# Usage: ./scripts/test.sh [site-name]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get site name
SITE_NAME=${1:-}

if [ -z "$SITE_NAME" ]; then
    echo -e "${RED}Error: Site name is required${NC}"
    echo "Usage: ./scripts/test.sh [site-name]"
    echo ""
    echo "Example: ./scripts/test.sh mysite.local"
    exit 1
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}BLKSHP OS Testing Script${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Site: ${GREEN}$SITE_NAME${NC}"
echo ""

# Navigate to bench directory
cd /Users/Eric/Development/BLKSHP/BLKSHP-DEV

# Check if app is installed on the site
echo -e "${YELLOW}→${NC} Checking if blkshp_os is installed on site..."
if ! bench --site $SITE_NAME list-apps | grep -q "blkshp_os"; then
    echo -e "${RED}✗${NC} App blkshp_os is not installed on site $SITE_NAME"
    echo ""
    echo -e "${YELLOW}Please install the app first:${NC}"
    echo -e "  ${BLUE}bench --site $SITE_NAME install-app blkshp_os${NC}"
    echo ""
    echo -e "See ${BLUE}docs/FIRST-TIME-SETUP.md${NC} for detailed instructions."
    exit 1
fi
echo -e "${GREEN}✓${NC} App is installed"
echo ""

# Function to run command with error handling
run_cmd() {
    local cmd=$1
    local desc=$2
    
    echo -e "${YELLOW}→${NC} $desc"
    if eval "$cmd"; then
        echo -e "${GREEN}✓${NC} Done"
        echo ""
    else
        echo -e "${RED}✗${NC} Failed"
        exit 1
    fi
}

# Step 1: Migrate (this also loads fixtures automatically)
run_cmd "bench --site $SITE_NAME migrate" "Running migrations and loading fixtures"

# Step 2: Clear cache
run_cmd "bench --site $SITE_NAME clear-cache" "Clearing cache"

# Step 3: Build assets
run_cmd "bench build --app blkshp_os" "Building assets"

# Step 4: Setup test data
echo -e "${YELLOW}→${NC} Setting up test data"
echo -e "${BLUE}Would you like to create test data? (y/n)${NC}"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    run_cmd "bench --site $SITE_NAME execute blkshp_os.scripts.setup_test_data.setup_all" "Creating test data"
else
    echo -e "${YELLOW}Skipped test data creation${NC}"
    echo ""
fi

# Step 5: Run tests
echo -e "${BLUE}Would you like to run unit tests? (y/n)${NC}"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    run_cmd "bench --site $SITE_NAME run-tests --app blkshp_os" "Running unit tests"
else
    echo -e "${YELLOW}Skipped unit tests${NC}"
    echo ""
fi

# Summary
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo ""
echo "1. Start the bench:"
echo -e "   ${YELLOW}bench start${NC}"
echo ""
echo "2. Access your site:"
echo -e "   ${YELLOW}http://localhost:8000${NC}"
echo ""
echo "3. Set passwords for test users:"
echo -e "   ${YELLOW}bench --site $SITE_NAME set-password buyer@test.com${NC}"
echo -e "   ${YELLOW}bench --site $SITE_NAME set-password inventory@test.com${NC}"
echo -e "   ${YELLOW}bench --site $SITE_NAME set-password manager@test.com${NC}"
echo ""
echo "4. Review the testing guide:"
echo -e "   ${YELLOW}apps/blkshp_os/docs/TESTING-GUIDE.md${NC}"
echo ""
echo -e "${GREEN}Happy Testing! 🧪${NC}"
echo ""

