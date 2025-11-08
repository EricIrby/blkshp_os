#!/usr/bin/env python3
"""
Setup Test Data for BLKSHP OS

This script creates sample data for testing the Departments and Permissions domains.

Usage:
    bench --site [your-site] execute blkshp_os.scripts.setup_test_data.setup_all
"""

import frappe
from frappe import _


def setup_all():
    """Setup all test data."""
    print("\n" + "="*60)
    print("Setting up BLKSHP OS Test Data")
    print("="*60 + "\n")
    
    try:
        setup_company()
        setup_departments()
        setup_test_users()
        setup_test_roles()
        
        frappe.db.commit()
        
        print("\n" + "="*60)
        print("✅ Test Data Setup Complete!")
        print("="*60 + "\n")
        print_summary()
        
    except Exception as e:
        frappe.db.rollback()
        print(f"\n❌ Error during setup: {str(e)}")
        raise


def setup_company():
    """Create a test company if it doesn't exist."""
    print("📊 Setting up test company...")
    
    company_name = "Test Restaurant"
    
    if frappe.db.exists("Company", company_name):
        print(f"   ℹ️  Company '{company_name}' already exists, skipping.")
        return
    
    company = frappe.get_doc({
        "doctype": "Company",
        "company_name": company_name,
        "abbr": "TR",
        "default_currency": "USD",
        "country": "United States"
    })
    company.insert(ignore_permissions=True)
    
    print(f"   ✅ Created company: {company_name}")


def setup_departments():
    """Create test departments."""
    print("\n🏢 Setting up test departments...")
    
    company = "Test Restaurant"
    
    departments = [
        {
            "department_name": "Kitchen",
            "department_code": "KITCHEN",
            "department_type": "Kitchen",
            "company": company,
            "is_active": 1,
            "settings": {
                "eoq_enabled": True,
                "default_ordering_day": "Monday",
                "minimum_order_amount": 100.0,
                "require_order_approval": False
            }
        },
        {
            "department_name": "Bar",
            "department_code": "BAR",
            "department_type": "Beverage",
            "company": company,
            "is_active": 1,
            "settings": {
                "eoq_enabled": True,
                "default_ordering_day": "Tuesday",
                "minimum_order_amount": 50.0,
                "require_order_approval": True
            }
        },
        {
            "department_name": "Catering",
            "department_code": "CATERING",
            "department_type": "Food",
            "company": company,
            "is_active": 1,
            "settings": {
                "eoq_enabled": False,
                "require_order_approval": True
            }
        },
        {
            "department_name": "Office",
            "department_code": "OFFICE",
            "department_type": "Office",
            "company": company,
            "is_active": 1
        },
        {
            "department_name": "Prep Kitchen",
            "department_code": "PREP",
            "department_type": "Kitchen",
            "company": company,
            "is_active": 1,
            "parent_department": "KITCHEN"
        }
    ]
    
    for dept_data in departments:
        dept_code = dept_data["department_code"]
        
        if frappe.db.exists("Department", dept_code):
            print(f"   ℹ️  Department '{dept_code}' already exists, skipping.")
            continue
        
        dept = frappe.get_doc({
            "doctype": "Department",
            **dept_data
        })
        dept.insert(ignore_permissions=True)
        
        print(f"   ✅ Created department: {dept_code}")


def setup_test_users():
    """Create test users with department permissions."""
    print("\n👥 Setting up test users...")
    
    users = [
        {
            "email": "buyer@test.com",
            "first_name": "Test",
            "last_name": "Buyer",
            "roles": ["Buyer"],
            "departments": [
                {
                    "department": "KITCHEN",
                    "can_read": 1,
                    "can_write": 1,
                    "can_create": 1,
                    "can_approve": 1,
                    "is_active": 1
                },
                {
                    "department": "BAR",
                    "can_read": 1,
                    "can_write": 1,
                    "can_create": 1,
                    "can_approve": 1,
                    "is_active": 1
                }
            ]
        },
        {
            "email": "inventory@test.com",
            "first_name": "Test",
            "last_name": "Inventory",
            "roles": ["Inventory Taker"],
            "departments": [
                {
                    "department": "KITCHEN",
                    "can_read": 1,
                    "can_write": 1,
                    "is_active": 1
                }
            ]
        },
        {
            "email": "manager@test.com",
            "first_name": "Test",
            "last_name": "Manager",
            "roles": ["Store Manager"],
            "departments": [
                {
                    "department": "KITCHEN",
                    "can_read": 1,
                    "can_write": 1,
                    "can_create": 1,
                    "can_delete": 1,
                    "can_submit": 1,
                    "can_cancel": 1,
                    "can_approve": 1,
                    "is_active": 1
                },
                {
                    "department": "BAR",
                    "can_read": 1,
                    "can_write": 1,
                    "can_create": 1,
                    "can_delete": 1,
                    "can_submit": 1,
                    "can_cancel": 1,
                    "can_approve": 1,
                    "is_active": 1
                },
                {
                    "department": "CATERING",
                    "can_read": 1,
                    "can_write": 1,
                    "can_create": 1,
                    "is_active": 1
                }
            ]
        }
    ]
    
    for user_data in users:
        email = user_data["email"]
        
        if frappe.db.exists("User", email):
            print(f"   ℹ️  User '{email}' already exists, skipping.")
            continue
        
        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": user_data["first_name"],
            "last_name": user_data["last_name"],
            "enabled": 1,
            "send_welcome_email": 0
        })
        
        # Add roles
        for role in user_data.get("roles", []):
            user.append("roles", {"role": role})
        
        # Add department permissions
        for dept_perm in user_data.get("departments", []):
            user.append("department_permissions", dept_perm)
        
        user.insert(ignore_permissions=True)
        
        print(f"   ✅ Created user: {email}")


def setup_test_roles():
    """Verify standard roles are set up."""
    print("\n🔐 Verifying standard roles...")
    
    standard_roles = [
        "Inventory Taker",
        "Inventory Administrator",
        "Recipe Builder",
        "Buyer",
        "Receiver",
        "Bartender",
        "Store Manager",
        "Director"
    ]
    
    for role_name in standard_roles:
        if frappe.db.exists("Role", role_name):
            role = frappe.get_doc("Role", role_name)
            perm_count = len(role.get("custom_permissions", []))
            print(f"   ✅ Role '{role_name}' exists with {perm_count} permissions")
        else:
            print(f"   ⚠️  Role '{role_name}' not found - run 'bench import-fixtures'")


def print_summary():
    """Print a summary of created data."""
    print("\n📋 Summary:")
    print("-" * 60)
    
    # Count departments
    dept_count = frappe.db.count("Department")
    print(f"   Departments: {dept_count}")
    
    # Count users
    user_count = frappe.db.count("User", filters={"email": ["like", "%@test.com"]})
    print(f"   Test Users: {user_count}")
    
    # Count roles with permissions
    role_count = frappe.db.count("Role", filters={"is_custom_role": 1})
    print(f"   Custom Roles: {role_count}")
    
    print("-" * 60)
    print("\n📚 Next Steps:")
    print("   1. Log in with any test user:")
    print("      - buyer@test.com")
    print("      - inventory@test.com")
    print("      - manager@test.com")
    print("   2. Set passwords using: bench --site [site] set-password [email]")
    print("   3. Test department access and permissions")
    print("   4. Review the TESTING-GUIDE.md for detailed test scenarios")
    print()


if __name__ == "__main__":
    setup_all()

