#!/bin/bash
# Helper script to merge current feature branch to main

CURRENT_BRANCH=$(git branch --show-current)

if [[ ! $CURRENT_BRANCH == feature/* ]]; then
    echo "❌ You must be on a feature branch to use this script"
    echo "Current branch: $CURRENT_BRANCH"
    exit 1
fi

echo "🔄 Merging $CURRENT_BRANCH into main..."

# Switch to main and update
git checkout main
if ! git pull origin main; then
    echo "⚠️  Could not pull latest changes from origin/main"
fi

# Merge feature branch
git merge $CURRENT_BRANCH --no-ff -m "Merge $CURRENT_BRANCH into main"

# Push to remote
git push origin main

echo "✅ Merged $CURRENT_BRANCH into main"
echo "💡 You can now switch back to your feature branch: git checkout $CURRENT_BRANCH"
