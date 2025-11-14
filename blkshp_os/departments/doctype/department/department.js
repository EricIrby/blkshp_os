// Department DocType client script
frappe.ui.form.on('Department', {
	refresh: function(frm) {
		// Add custom buttons
		if (!frm.is_new()) {
			frm.add_custom_button(__('View Products'), function() {
				frappe.set_route('List', 'Product', {
					'departments.department': frm.doc.name
				});
			}, __('View'));

			frm.add_custom_button(__('View Users'), function() {
				frappe.set_route('List', 'User', {
					'department_permissions.department': frm.doc.name
				});
			}, __('View'));

			// Add button to view department inventory
			frm.add_custom_button(__('View Inventory'), function() {
				frappe.set_route('query-report', 'Inventory Balance', {
					'department': frm.doc.name
				});
			}, __('View'));
		}

		// Set indicator based on active status
		if (frm.doc.is_active) {
			frm.dashboard.set_headline_alert(__('Active Department'), 'green');
		} else {
			frm.dashboard.set_headline_alert(__('Inactive Department'), 'red');
		}
	},

	department_code: function(frm) {
		// Auto-uppercase department code
		if (frm.doc.department_code) {
			frm.set_value('department_code', frm.doc.department_code.toUpperCase());
		}
	},

	company: function(frm) {
		// Clear parent department if company changes
		if (frm.doc.parent_department) {
			frappe.db.get_value('Department', frm.doc.parent_department, 'company', function(r) {
				if (r && r.message && r.message.company !== frm.doc.company) {
					frappe.msgprint(__('Parent department belongs to a different company. Clearing parent department.'));
					frm.set_value('parent_department', '');
				}
			});
		}
	},

	parent_department: function(frm) {
		// Validate parent department belongs to same company
		if (frm.doc.parent_department && frm.doc.company) {
			frappe.db.get_value('Department', frm.doc.parent_department, 'company', function(r) {
				if (r && r.message && r.message.company !== frm.doc.company) {
					frappe.msgprint(__('Parent department must belong to the same company.'));
					frm.set_value('parent_department', '');
				}
			});
		}

		// Prevent self-reference
		if (frm.doc.parent_department === frm.doc.name) {
			frappe.msgprint(__('A department cannot be its own parent.'));
			frm.set_value('parent_department', '');
		}
	},

	is_active: function(frm) {
		// Warn if deactivating department
		if (!frm.doc.is_active && !frm.is_new()) {
			frappe.warn(__('Deactivating Department'),
				__('Deactivating this department will affect user access and product assignments. Are you sure?'),
				function() {
					// User confirmed
					frm.save();
				},
				function() {
					// User cancelled
					frm.set_value('is_active', 1);
				}
			);
		}
	}
});

