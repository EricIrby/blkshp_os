#!/usr/bin/env python3
"""
Manually sync DocTypes to database.

Usage:
    bench --site [your-site] execute blkshp_os.scripts.sync_doctypes.sync_all
"""

import frappe
from frappe.modules.import_file import import_file_by_path
import os


def sync_all():
    """Sync all BLKSHP OS DocTypes to the database."""
    print("\n" + "="*60)
    print("Syncing BLKSHP OS DocTypes")
    print("="*60 + "\n")
    
    # Get the app path
    app_path = frappe.get_app_path("blkshp_os")
    
    doctypes = {
        "department": ("departments", "department"),
        "product_department": ("departments", "product_department"),
        "department_permission": ("permissions", "department_permission"),
        "role_permission": ("permissions", "role_permission"),
    }
    
    for doctype, (module_name, folder_name) in doctypes.items():
        json_path = os.path.join(app_path, module_name, "doctype", folder_name, f"{doctype}.json")
        
        if os.path.exists(json_path):
            print(f"Syncing {doctype}...")
            try:
                import_file_by_path(json_path)
                print(f"  ✅ {doctype} synced successfully")
            except Exception as e:
                print(f"  ❌ Error syncing {doctype}: {str(e)}")
        else:
            print(f"  ⚠️  JSON file not found: {json_path}")
    
    frappe.db.commit()
    
    print("\n" + "="*60)
    print("Verifying DocTypes...")
    print("="*60 + "\n")
    
    # Verify
    for doctype in doctypes.keys():
        doctype_name = doctype.replace("_", " ").title()
        exists = frappe.db.exists("DocType", doctype_name)
        status = "✅" if exists else "❌"
        print(f"{status} {doctype_name}: {exists}")
    
    print("\n" + "="*60)
    print("Sync Complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    sync_all()

