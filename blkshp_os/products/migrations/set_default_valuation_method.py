"""
Migration script to set default valuation method for existing products.

This script ensures all existing Product records have:
- valuation_method set to "Moving Average" (default)
- valuation_rate initialized to 0.00

Run with: bench execute blkshp_os.products.migrations.set_default_valuation_method.execute
"""

import frappe


def execute():
    """Set default valuation method for all existing products."""
    frappe.reload_doctype("Product")

    # Get all products without valuation_method set
    products = frappe.get_all(
        "Product",
        filters=[
            ["valuation_method", "in", [None, ""]],
        ],
        fields=["name", "product_name"],
    )

    if not products:
        print("No products found requiring migration.")
        return

    print(f"Migrating {len(products)} products to set default valuation method...")

    updated_count = 0
    for product in products:
        try:
            doc = frappe.get_doc("Product", product.name)

            # Set defaults
            if not doc.valuation_method:
                doc.valuation_method = "Moving Average"

            if doc.valuation_rate is None:
                doc.valuation_rate = 0.0

            # Save without triggering hooks
            doc.save(ignore_permissions=True)
            updated_count += 1

            if updated_count % 100 == 0:
                print(f"Migrated {updated_count} products...")
                frappe.db.commit()

        except Exception as e:
            print(f"Error migrating product {product.name}: {str(e)}")
            continue

    frappe.db.commit()
    print(f"✅ Successfully migrated {updated_count} products.")
    print(f"   - Set valuation_method to 'Moving Average'")
    print(f"   - Initialized valuation_rate to 0.00")


if __name__ == "__main__":
    execute()
