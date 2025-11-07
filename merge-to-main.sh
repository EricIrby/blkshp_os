#!/bin/bash
# Helper script to merge current feature branch to main

CURRENT_BRANCH=$(git branch --show-current)

if [[ ! $CURRENT_BRANCH == feature/* ]]; then
    echo "❌ You must be on a feature branch to use this script"
    echo "Current branch: $CURRENT_BRANCH"
    exit 1
fi

echo "🔄 Merging $CURRENT_BRANCH to main..."

# Switch to main and update
git checkout main
git pull origin main

# Merge feature branch
git merge $CURRENT_BRANCH --no-ff -m "Merge $CURRENT_BRANCH into main"

# Push to remote
git push origin main

echo "✅ Merged $CURRENT_BRANCH to main"
echo "💡 You can now switch back to your feature branch: git checkout $CURRENT_BRANCH"
