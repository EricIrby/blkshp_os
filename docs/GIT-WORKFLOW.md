# Git Development Workflow

## Branch Strategy

### Main Branch
- `main` - Production-ready code
- All completed features are merged here
- Protected branch (requires PR for merges)
- Only documentation updates should be committed directly

### Feature Branches
- `feature/<domain>` - Domain-specific development branches
- Each domain has its own feature branch
- Work independently on each domain
- Merge to main when domain is complete

## Development Workflow

### Starting Work on a Domain

```bash
# 1. Switch to the domain branch
./switch-domain.sh departments

# 2. Pull latest changes (if working with others)
git pull origin feature/departments

# 3. Create a sub-feature branch for specific work (optional)
git checkout -b feature/departments-permissions

# 4. Make your changes
# ... edit files ...

# 5. Commit your changes
git add .
git commit -m "feat(departments): Add department permissions functionality"

# 6. Push to remote
git push origin feature/departments-permissions
```

### Committing Changes

**Commit Message Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
git commit -m "feat(departments): Add department allocation functionality"
git commit -m "fix(inventory): Fix theoretical inventory calculation"
git commit -m "docs(products): Update unit conversion documentation"
```

### Merging to Main

**Option 1: Using Helper Script**
```bash
# On your feature branch
./merge-to-main.sh
```

**Option 2: Manual Merge**
```bash
# 1. Ensure your feature branch is up to date
git checkout feature/departments
git pull origin feature/departments

# 2. Switch to main and update
git checkout main
git pull origin main

# 3. Merge feature branch
git merge feature/departments --no-ff -m "Merge feature/departments into main"

# 4. Push to remote
git push origin main

# 5. Switch back to feature branch
git checkout feature/departments
```

### Working with Multiple Domains

```bash
# Work on departments
./switch-domain.sh departments
# ... make changes ...
git commit -m "feat(departments): ..."
git push origin feature/departments

# Switch to products
./switch-domain.sh products
# ... make changes ...
git commit -m "feat(products): ..."
git push origin feature/products
```

## Best Practices

### 1. Always Work on Feature Branches
- Never commit directly to `main` (except documentation)
- Use feature branches for all development work
- Keep feature branches focused on one domain

### 2. Commit Frequently
- Commit small, logical changes
- Write clear commit messages
- Push regularly to backup your work

### 3. Keep Branches Up to Date
- Pull latest changes before starting work
- Rebase or merge main into feature branch if needed
- Resolve conflicts early

### 4. Use Descriptive Commit Messages
- Follow the commit message format
- Explain what and why, not just what
- Reference issues/tickets if applicable

### 5. Test Before Merging
- Test your changes thoroughly
- Run any existing tests
- Verify integration with other domains

## Common Tasks

### View Branch Status
```bash
# See current branch
git branch --show-current

# See all branches
git branch -a

# See remote branches
git branch -r
```

### Update Feature Branch from Main
```bash
# On your feature branch
git checkout feature/departments

# Merge latest main into your branch
git merge main

# Or rebase (cleaner history)
git rebase main
```

### Stash Changes
```bash
# Save current changes without committing
git stash

# Switch branches
git checkout main

# Return to feature branch and restore changes
git checkout feature/departments
git stash pop
```

### View Changes
```bash
# See what files changed
git status

# See detailed changes
git diff

# See changes in staged files
git diff --cached

# See commit history
git log --oneline --graph --all -20
```

## Troubleshooting

### Accidentally Committed to Main
```bash
# Create a feature branch from current state
git branch feature/my-feature

# Reset main to previous commit
git checkout main
git reset --hard HEAD~1

# Switch to feature branch
git checkout feature/my-feature
```

### Need to Undo Last Commit
```bash
# Undo commit but keep changes
git reset --soft HEAD~1

# Undo commit and discard changes (careful!)
git reset --hard HEAD~1
```

### Merge Conflicts
```bash
# When merge conflict occurs:
# 1. Open conflicted files
# 2. Resolve conflicts (look for <<<<<< markers)
# 3. Stage resolved files
git add <resolved-file>

# 4. Complete the merge
git commit
```

## Helper Scripts

- `./switch-domain.sh <domain>` - Switch to domain feature branch
- `./new-feature.sh <feature-name>` - Create new feature branch
- `./merge-to-main.sh` - Merge current branch to main

## Next Steps

1. Start with the Departments domain (foundation)
2. Follow the development guide in `docs/START-HERE.md`
3. Use feature branches for all development work
4. Commit and push regularly

