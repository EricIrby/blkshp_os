#!/bin/bash
# Helper script to switch between domain branches

DOMAIN=$1

if [ -z "$DOMAIN" ]; then
    echo "Usage: ./switch-domain.sh <domain>"
    echo ""
    echo "Available domains:"
    echo "  - architecture"
    echo "  - departments"
    echo "  - products"
    echo "  - inventory"
    echo "  - procurement"
    echo "  - recipes"
    echo "  - pos-integration"
    echo "  - accounting"
    echo "  - analytics"
    echo "  - director"
    echo "  - transfers-depletions"
    echo "  - payments"
    echo "  - permissions"
    echo "  - budgets"
    exit 1
fi

BRANCH="feature/$DOMAIN"

# Check if branch exists
if ! git show-ref --verify --quiet refs/heads/$BRANCH; then
    echo "❌ Branch $BRANCH does not exist"
    echo "Available branches:"
    git branch | grep feature/
    exit 1
fi

# Switch to the branch
git checkout $BRANCH

declare -A DOMAIN_DIRS=(
    [departments]="departments"
    [products]="products"
    [inventory]="inventory"
    [procurement]="procurement"
    [recipes]="recipes"
    [pos-integration]="pos_integration"
    [accounting]="accounting"
    [analytics]="analytics"
    [director]="director"
    [transfers-depletions]="transfers_depletions"
    [payments]="payments"
    [permissions]="permissions"
    [budgets]="budgets"
)

MODULE_DIR="${DOMAIN_DIRS[$DOMAIN]}"

if [ -n "$MODULE_DIR" ]; then
    echo "✅ Switched to $BRANCH branch"
    echo "📁 Domain directory: blkshp_os/blkshp_os/modules/$MODULE_DIR/"
    echo ""
    echo "💡 Tip: Only commit files from the $MODULE_DIR module directory on this branch"
else
    echo "✅ Switched to $BRANCH branch"
fi
