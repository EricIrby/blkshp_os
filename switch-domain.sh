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
if git show-ref --verify --quiet refs/heads/$BRANCH; then
    git checkout $BRANCH
    echo "✅ Switched to $BRANCH branch"
else
    echo "❌ Branch $BRANCH does not exist"
    echo "Available branches:"
    git branch | grep feature/
    exit 1
fi
