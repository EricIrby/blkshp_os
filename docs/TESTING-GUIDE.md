# Testing Guide - BLKSHP OS

## Overview

This guide will walk you through testing the Departments and Permissions domains on your local Frappe instance.

---

## Prerequisites

Before testing, ensure you have:

1. **Frappe Framework** installed (v14 or v15 recommended)
2. **Frappe Bench** set up
3. **A test site** created
4. **BLKSHP OS app** installed on your site

---

## Step 1: Install/Update the App

### Option A: Fresh Installation

If you haven't installed the app yet:

```bash
# Navigate to your bench directory
cd /Users/Eric/Development/BLKSHP/BLKSHP-DEV

# Install the app on your site
bench --site [your-site-name] install-app blkshp_os

# Run migrations
bench --site [your-site-name] migrate

# Clear cache
bench --site [your-site-name] clear-cache
```

### Option B: Update Existing Installation

If the app is already installed:

```bash
# Navigate to your bench directory
cd /Users/Eric/Development/BLKSHP/BLKSHP-DEV

# Pull latest changes (already done via git)
cd apps/blkshp_os
git pull origin main
cd ../..

# Run migrations to create new DocTypes
# Note: This also automatically loads fixtures (custom fields and standard roles)
bench --site [your-site-name] migrate

# Clear cache and restart
bench --site [your-site-name] clear-cache
bench restart
```

---

## Step 2: Verify Installation

### Check DocTypes Created

```bash
# List all DocTypes in the app
bench --site [your-site-name] console

# In the console:
>>> frappe.get_all("DocType", filters={"module": ["in", ["Departments", "Permissions"]]}, fields=["name", "module"])
```

**Expected DocTypes:**
- Department (Departments module)
- Department Permission (Permissions module)
- Product Department (Departments module)
- Role Permission (Permissions module)

### Check Custom Fields

```bash
# Check if custom fields were created
bench --site [your-site-name] console

# In the console:
>>> frappe.get_all("Custom Field", filters={"dt": ["in", ["User", "Role"]]}, fields=["name", "fieldname", "dt"])
```

**Expected Custom Fields:**
- User-department_permissions
- User-is_team_account
- Role-custom_permissions
- Role-is_custom_role
- Role-role_description

---

## Step 3: Start the Development Server

```bash
# Start the bench
bench start

# Or if you want to run in the background:
bench start &
```

Access your site at: `http://localhost:8000` (or your configured port)

---

## Step 4: Test Departments Domain

### 4.1 Create a Test Company

1. Log in as Administrator
2. Go to: **Home → Accounting → Company**
3. Create a new company:
   - Company Name: "Test Restaurant"
   - Default Currency: USD
   - Save

### 4.2 Create Departments

1. Go to: **Home → Departments → Department**
2. Click **New**
3. Create your first department:
   - Department Name: "Kitchen"
   - Department Code: "KITCHEN"
   - Department Type: "Kitchen"
   - Company: "Test Restaurant"
   - Is Active: ✓
   - Save

4. Create more departments:
   - Bar (BAR, Beverage)
   - Catering (CATERING, Food)
   - Office (OFFICE, Office)

### 4.3 Test Department Hierarchy

1. Create a sub-department:
   - Department Name: "Prep Kitchen"
   - Department Code: "PREP"
   - Department Type: "Kitchen"
   - Company: "Test Restaurant"
   - Parent Department: "Kitchen"
   - Save

2. Verify the hierarchy is displayed correctly

### 4.4 Test Department Settings

1. Open the "Kitchen" department
2. In the Settings section, add JSON settings:

```json
{
  "eoq_enabled": true,
  "default_ordering_day": "Monday",
  "minimum_order_amount": 100.0,
  "require_order_approval": false
}
```

3. Save and verify no validation errors

### 4.5 Test Department API

Open your browser console and test the API:

```javascript
// Get accessible departments
frappe.call({
    method: 'blkshp_os.api.departments.get_accessible_departments',
    callback: function(r) {
        console.log('Accessible Departments:', r.message);
    }
});

// Get department details
frappe.call({
    method: 'blkshp_os.api.departments.get_department_details',
    args: {
        department: 'KITCHEN'
    },
    callback: function(r) {
        console.log('Department Details:', r.message);
    }
});

// Get department statistics
frappe.call({
    method: 'blkshp_os.api.departments.get_department_statistics',
    args: {
        department: 'KITCHEN'
    },
    callback: function(r) {
        console.log('Department Statistics:', r.message);
    }
});
```

---

## Step 5: Test Permissions Domain

### 5.1 View Available Permissions

1. Open browser console
2. Run:

```javascript
frappe.call({
    method: 'blkshp_os.api.roles.get_available_permissions',
    callback: function(r) {
        console.log('Available Permissions:', r.message);
        console.log('Total:', r.message.length);
    }
});
```

**Expected:** 68 permissions

### 5.2 View Permission Categories

```javascript
frappe.call({
    method: 'blkshp_os.api.roles.get_permission_categories',
    callback: function(r) {
        console.log('Permission Categories:', r.message);
    }
});
```

**Expected Categories:**
- Orders, Invoices, Audits, Items, Vendors, Recipes, Transfers, Depletions, Reports, System, Director

### 5.3 Create a Custom Role

1. Go to: **Home → Users and Permissions → Role**
2. Click **New**
3. Create a custom role:
   - Role Name: "Test Buyer"
   - Is Custom Role: ✓
   - Role Description: "Test role for buyers"
   - Desk Access: ✓
   - Save

4. In the **Custom Permissions** table, click **Add Permissions** button
5. Select permissions:
   - orders.view
   - orders.create
   - orders.place
   - vendors.view
   - items.view
6. Save

### 5.4 Test Role Summary

1. Open the "Test Buyer" role
2. Click **View → Role Summary**
3. Verify the summary shows:
   - Permission count: 5
   - Permissions by category

### 5.5 Assign Role to User

1. Go to: **Home → Users and Permissions → User**
2. Open your test user (or create one)
3. In the **Roles** table, add "Test Buyer"
4. Save

### 5.6 Test Department Permissions

1. Open the same user
2. Scroll to **Department Permissions** section
3. Add a new row:
   - Department: "Kitchen"
   - Can Read: ✓
   - Can Write: ✓
   - Is Active: ✓
4. Save

### 5.7 Test Permission Checking

```javascript
// Check if current user has a permission
frappe.call({
    method: 'blkshp_os.api.roles.check_permission',
    args: {
        permission_code: 'orders.view'
    },
    callback: function(r) {
        console.log('Has orders.view permission:', r.message);
    }
});

// Get all user permissions
frappe.call({
    method: 'blkshp_os.api.roles.get_user_permissions',
    callback: function(r) {
        console.log('User Permissions:', r.message);
    }
});
```

---

## Step 6: Run Unit Tests

### Run All Tests

```bash
# Run all tests for the app
bench --site [your-site-name] run-tests --app blkshp_os

# Run tests with verbose output
bench --site [your-site-name] run-tests --app blkshp_os --verbose
```

### Run Specific Test Modules

```bash
# Test Department DocType
bench --site [your-site-name] run-tests --module blkshp_os.departments.doctype.department.test_department

# Test Department Permission
bench --site [your-site-name] run-tests --module blkshp_os.permissions.doctype.department_permission.test_department_permission

# Test Role Permission
bench --site [your-site-name] run-tests --module blkshp_os.permissions.doctype.role_permission.test_role_permission

# Test Permissions Service
bench --site [your-site-name] run-tests --module blkshp_os.permissions.test_permissions_service

# Test Roles Service
bench --site [your-site-name] run-tests --module blkshp_os.permissions.test_roles
```

---

## Step 7: Test Standard Roles

### Import Standard Roles

The standard roles should be imported automatically via fixtures. If not:

```bash
# Import fixtures manually
bench --site [your-site-name] import-fixtures
```

### Verify Standard Roles

1. Go to: **Home → Users and Permissions → Role**
2. Check for these roles:
   - Inventory Taker
   - Inventory Administrator
   - Recipe Builder
   - Buyer
   - Receiver
   - Bartender
   - Store Manager
   - Director

3. Open each role and verify:
   - Is Custom Role: ✓
   - Role Description is populated
   - Custom Permissions table has permissions

---

## Step 8: Test Client Scripts

### Test Department Form

1. Open any Department
2. Verify custom buttons appear:
   - **View → View Products**
   - **View → View Users**
   - **View → View Inventory**
3. Click each button and verify they work

### Test Role Form

1. Open any Role with custom permissions
2. Verify custom buttons appear:
   - **View → View Users**
   - **View → Role Summary**
   - **Actions → Add Permissions**
3. Click **Add Permissions** and verify:
   - Dialog opens with permission selector
   - Permissions grouped by category
   - Can select and add permissions

### Test User Form

1. Open any User with department permissions
2. Verify custom button appears:
   - **Departments → View Accessible Departments**
3. Click and verify it shows the list

---

## Step 9: Test REST API Endpoints

### Using Postman or cURL

Get your API key and secret:
1. Go to your User profile
2. Click **API Access**
3. Generate API Key/Secret

### Test Department Endpoints

```bash
# Get accessible departments
curl -X GET "http://localhost:8000/api/method/blkshp_os.api.departments.get_accessible_departments" \
  -H "Authorization: token YOUR_API_KEY:YOUR_API_SECRET"

# Get department details
curl -X POST "http://localhost:8000/api/method/blkshp_os.api.departments.get_department_details" \
  -H "Authorization: token YOUR_API_KEY:YOUR_API_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"department": "KITCHEN"}'
```

### Test Role Endpoints

```bash
# Get available permissions
curl -X GET "http://localhost:8000/api/method/blkshp_os.api.roles.get_available_permissions" \
  -H "Authorization: token YOUR_API_KEY:YOUR_API_SECRET"

# Check permission
curl -X POST "http://localhost:8000/api/method/blkshp_os.api.roles.check_permission" \
  -H "Authorization: token YOUR_API_KEY:YOUR_API_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"permission_code": "orders.view"}'
```

---

## Step 10: Test Permission Enforcement

### Test Department-Based Access

1. Create a test user: "buyer@test.com"
2. Assign role: "Buyer"
3. Assign department permission: Kitchen (can_read, can_write)
4. Log in as this user
5. Verify:
   - Can only see "Kitchen" department in list
   - Cannot see other departments

### Test Role-Based Access

1. Log in as a user with "Inventory Taker" role
2. Verify:
   - Has audits.view permission
   - Has audits.do permission
   - Does NOT have orders.create permission

---

## Troubleshooting

### Issue: DocTypes Not Created

**Solution:**
```bash
bench --site [your-site-name] migrate
bench --site [your-site-name] clear-cache
bench restart
```

### Issue: Custom Fields Not Showing

**Solution:**
```bash
# Fixtures are loaded during migrate, so run migrate again
bench --site [your-site-name] migrate --skip-search-index
bench --site [your-site-name] clear-cache
bench restart
```

### Issue: Client Scripts Not Loading

**Solution:**
```bash
# Build assets
bench build --app blkshp_os

# Or clear cache
bench --site [your-site-name] clear-cache
bench --site [your-site-name] clear-website-cache
```

### Issue: Permission Errors

**Solution:**
1. Ensure you're logged in as Administrator or System Manager
2. Check that the user has the required role
3. Verify department permissions are set correctly

### Issue: Tests Failing

**Solution:**
```bash
# Reinstall the app
bench --site [your-site-name] reinstall

# Run migrations
bench --site [your-site-name] migrate

# Run tests again
bench --site [your-site-name] run-tests --app blkshp_os
```

---

## Quick Test Checklist

Use this checklist to verify everything is working:

### Departments Domain
- [ ] Can create departments
- [ ] Can create department hierarchy
- [ ] Can add JSON settings
- [ ] Department form buttons work
- [ ] Department API endpoints work
- [ ] Department permission filtering works

### Permissions Domain
- [ ] Can view 68 permissions
- [ ] Can create custom roles
- [ ] Can assign permissions to roles
- [ ] Can assign roles to users
- [ ] Can assign department permissions to users
- [ ] Role form buttons work
- [ ] Permission checking works
- [ ] Standard roles are imported

### Tests
- [ ] All unit tests pass
- [ ] Department tests pass
- [ ] Permission tests pass
- [ ] Role tests pass

---

## Next Steps

Once testing is complete:

1. **Document any issues** found
2. **Create test data** for other domains
3. **Move to Products domain** development
4. **Set up CI/CD** for automated testing

---

## Support

If you encounter issues:

1. Check the Frappe error logs: `bench --site [your-site-name] logs`
2. Review the implementation summaries in `docs/`
3. Check the API reference: `docs/API-REFERENCE.md`
4. Review test files for usage examples

---

**Happy Testing! 🧪**

