#!/bin/bash
# Helper script to create a new feature branch from main

FEATURE=$1

if [ -z "$FEATURE" ]; then
    echo "Usage: ./new-feature.sh <feature-name>"
    echo "Example: ./new-feature.sh departments-permissions"
    exit 1
fi

BRANCH="feature/$FEATURE"

# Ensure we're on main and up to date
git checkout main
if ! git pull origin main; then
    echo "⚠️  Could not pull latest changes from origin/main"
fi

# Create new feature branch
git checkout -b $BRANCH

echo "✅ Created and switched to $BRANCH branch"
echo "💡 When ready, push with: git push -u origin $BRANCH"
