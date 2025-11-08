# Fixtures in BLKSHP OS

## What are Fixtures?

Fixtures are pre-defined data that get automatically loaded into your Frappe site. In BLKSHP OS, we use fixtures for:

1. **Custom Fields** - Extensions to User and Role DocTypes
2. **Standard Roles** - Pre-configured roles with permissions (future implementation)

---

## How Fixtures Work in Frappe

### Automatic Loading

Fixtures are **automatically loaded** when you run:

```bash
bench --site [your-site] migrate
```

There is **NO** separate `import-fixtures` command. The `migrate` command:
1. Creates/updates DocTypes
2. Runs database migrations
3. **Automatically loads fixtures** defined in `hooks.py`

### Where Fixtures are Defined

#### 1. hooks.py Configuration

```python
# blkshp_os/hooks.py
fixtures = [
    {
        "dt": "Custom Field",
        "filters": [
            ["name", "in", [
                "User-department_permissions",
                "User-is_team_account",
                "Role-custom_permissions",
                "Role-is_custom_role",
                "Role-role_description"
            ]],
        ],
    }
]
```

#### 2. Fixture JSON Files

Fixture data is stored in the `fixtures/` directory:
- `fixtures/custom_field.json` - Custom field definitions
- `fixtures/standard_roles.json` - Standard role templates (future)

---

## How to Load/Reload Fixtures

### First Time Installation

```bash
# Install the app
bench --site [your-site] install-app blkshp_os

# Migrate (loads fixtures automatically)
bench --site [your-site] migrate
```

### After Updating Fixtures

If you've modified fixture files or added new ones:

```bash
# Run migrate to reload fixtures
bench --site [your-site] migrate --skip-search-index

# Clear cache
bench --site [your-site] clear-cache

# Restart bench
bench restart
```

---

## How to Export Fixtures

If you need to export fixtures (e.g., after manually creating custom fields):

```bash
# Export all fixtures defined in hooks.py
bench --site [your-site] export-fixtures
```

This will update the JSON files in the `fixtures/` directory.

---

## Current Fixtures in BLKSHP OS

### Custom Fields (5 fields)

#### User DocType
1. **department_permissions** (Table)
   - Child DocType: Department Permission
   - Stores user's department-level permissions

2. **is_team_account** (Check)
   - Marks accounts used by teams vs individuals

#### Role DocType
3. **custom_permissions** (Table)
   - Child DocType: Role Permission
   - Stores granular permissions for the role

4. **is_custom_role** (Check)
   - Distinguishes custom roles from system roles

5. **role_description** (Text)
   - Describes the role's purpose and responsibilities

---

## Verifying Fixtures Loaded

### Check Custom Fields

```bash
bench --site [your-site] console
```

```python
# In the console
>>> frappe.get_all("Custom Field", 
...     filters={"dt": ["in", ["User", "Role"]]}, 
...     fields=["name", "fieldname", "dt"])
```

**Expected Output:**
```python
[
    {'name': 'User-department_permissions', 'fieldname': 'department_permissions', 'dt': 'User'},
    {'name': 'User-is_team_account', 'fieldname': 'is_team_account', 'dt': 'User'},
    {'name': 'Role-custom_permissions', 'fieldname': 'custom_permissions', 'dt': 'Role'},
    {'name': 'Role-is_custom_role', 'fieldname': 'is_custom_role', 'dt': 'Role'},
    {'name': 'Role-role_description', 'fieldname': 'role_description', 'dt': 'Role'}
]
```

### Check in UI

1. Go to: **Home → Users and Permissions → User**
2. Open any user
3. You should see:
   - **Department Permissions** section (table)
   - **Is Team Account** checkbox

4. Go to: **Home → Users and Permissions → Role**
5. Open any role
6. You should see:
   - **Custom Permissions** section (table)
   - **Is Custom Role** checkbox
   - **Role Description** field

---

## Troubleshooting

### Issue: Fixtures Not Loading

**Symptom:** Custom fields don't appear after migrate

**Solution:**
```bash
# Force reload fixtures
bench --site [your-site] migrate --skip-search-index

# Clear all caches
bench --site [your-site] clear-cache
bench --site [your-site] clear-website-cache

# Restart
bench restart
```

### Issue: Fixtures Partially Loaded

**Symptom:** Some custom fields appear but not all

**Solution:**
```bash
# Check for errors in the migrate log
bench --site [your-site] migrate

# If errors, check the fixture JSON files for syntax errors
cat fixtures/custom_field.json | python -m json.tool

# Reload
bench --site [your-site] migrate --skip-search-index
bench restart
```

### Issue: Old Fixture Data Persists

**Symptom:** Deleted fixture data still appears in the site

**Solution:**
```bash
# Fixtures don't auto-delete. You need to manually delete:
bench --site [your-site] console

# In console:
>>> frappe.delete_doc("Custom Field", "User-old_field_name", force=1)
>>> frappe.db.commit()
```

---

## Best Practices

1. **Always use migrate** - Never manually create data that should be in fixtures
2. **Export after manual changes** - If you create custom fields manually, export them
3. **Version control fixtures** - Always commit fixture JSON files to git
4. **Test on fresh site** - Verify fixtures load correctly on a clean installation
5. **Document fixture changes** - Update this file when adding new fixtures

---

## Common Commands Reference

```bash
# Load fixtures (via migrate)
bench --site [site] migrate

# Export fixtures to JSON
bench --site [site] export-fixtures

# Clear cache after fixture changes
bench --site [site] clear-cache

# Restart after fixture changes
bench restart

# Check fixture files
ls -la fixtures/
cat fixtures/custom_field.json
```

---

## Future Fixtures

Planned fixtures for future implementation:

- **Standard Roles** - Pre-configured roles with permissions
  - Inventory Taker
  - Inventory Administrator
  - Recipe Builder
  - Buyer
  - Receiver
  - Bartender
  - Store Manager
  - Director

These will be added to `fixtures/standard_roles.json` and loaded automatically via migrate.

---

**Remember:** There is no `import-fixtures` command in Frappe. Fixtures are automatically loaded during `migrate`!

