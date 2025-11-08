// User DocType client script extensions for department permissions
frappe.ui.form.on('User', {
	refresh: function(frm) {
		// Add custom button to view accessible departments
		if (!frm.is_new()) {
			frm.add_custom_button(__('View Accessible Departments'), function() {
				frappe.call({
					method: 'blkshp_os.api.departments.get_accessible_departments',
					args: {
						permission_flag: 'can_read'
					},
					callback: function(r) {
						if (r.message && r.message.length > 0) {
							let dept_list = r.message.map(d => 
								`<li><strong>${d.department_code}</strong> - ${d.department_name} (${d.company})</li>`
							).join('');
							frappe.msgprint({
								title: __('Accessible Departments'),
								message: __('User has access to {0} department(s):', [r.message.length]) + '<br><br><ul>' +
									dept_list + '</ul>',
								indicator: 'blue',
								wide: true
							});
						} else {
							frappe.msgprint({
								title: __('Accessible Departments'),
								message: __('User has no accessible departments.'),
								indicator: 'orange'
							});
						}
					}
				});
			}, __('Departments'));
		}
	}
});

// Department Permission child table handlers
frappe.ui.form.on('Department Permission', {
	department: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		
		// Validate department is active
		if (row.department) {
			frappe.db.get_value('Department', row.department, ['is_active', 'department_name'], function(r) {
				if (r && r.message) {
					if (!r.message.is_active) {
						frappe.msgprint(__('Warning: Department {0} is inactive.', [r.message.department_name]));
					}
				}
			});
		}
	},

	department_permissions_add: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		// Set default permission to read
		frappe.model.set_value(cdt, cdn, 'can_read', 1);
		frappe.model.set_value(cdt, cdn, 'is_active', 1);
	},

	can_read: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		// If read is unchecked, warn about removing all permissions
		if (!row.can_read && !row.can_write && !row.can_create && !row.can_delete && 
			!row.can_submit && !row.can_cancel && !row.can_approve) {
			frappe.msgprint(__('At least one permission must be selected.'));
			frappe.model.set_value(cdt, cdn, 'can_read', 1);
		}
	},

	can_write: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		// If write is checked, automatically check read
		if (row.can_write && !row.can_read) {
			frappe.model.set_value(cdt, cdn, 'can_read', 1);
			frappe.msgprint(__('Read permission automatically granted with write permission.'));
		}
	},

	can_create: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		// If create is checked, automatically check read and write
		if (row.can_create) {
			if (!row.can_read) {
				frappe.model.set_value(cdt, cdn, 'can_read', 1);
			}
			if (!row.can_write) {
				frappe.model.set_value(cdt, cdn, 'can_write', 1);
			}
			if (!row.can_read || !row.can_write) {
				frappe.msgprint(__('Read and write permissions automatically granted with create permission.'));
			}
		}
	},

	can_delete: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		// If delete is checked, automatically check read and write
		if (row.can_delete) {
			if (!row.can_read) {
				frappe.model.set_value(cdt, cdn, 'can_read', 1);
			}
			if (!row.can_write) {
				frappe.model.set_value(cdt, cdn, 'can_write', 1);
			}
			if (!row.can_read || !row.can_write) {
				frappe.msgprint(__('Read and write permissions automatically granted with delete permission.'));
			}
		}
	},

	can_submit: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		// If submit is checked, automatically check read and write
		if (row.can_submit) {
			if (!row.can_read) {
				frappe.model.set_value(cdt, cdn, 'can_read', 1);
			}
			if (!row.can_write) {
				frappe.model.set_value(cdt, cdn, 'can_write', 1);
			}
			if (!row.can_read || !row.can_write) {
				frappe.msgprint(__('Read and write permissions automatically granted with submit permission.'));
			}
		}
	},

	can_cancel: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		// If cancel is checked, automatically check read
		if (row.can_cancel && !row.can_read) {
			frappe.model.set_value(cdt, cdn, 'can_read', 1);
			frappe.msgprint(__('Read permission automatically granted with cancel permission.'));
		}
	},

	can_approve: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		// If approve is checked, automatically check read
		if (row.can_approve && !row.can_read) {
			frappe.model.set_value(cdt, cdn, 'can_read', 1);
			frappe.msgprint(__('Read permission automatically granted with approve permission.'));
		}
	},

	valid_from: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		// Validate valid_from is not in the future if not intended
		if (row.valid_from) {
			let valid_from = frappe.datetime.str_to_obj(row.valid_from);
			let today = frappe.datetime.now_date(true);
			if (valid_from > today) {
				frappe.msgprint(__('Note: This permission will only be effective from {0}.', [frappe.datetime.str_to_user(row.valid_from)]));
			}
		}
	},

	valid_upto: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		// Validate valid_upto is after valid_from
		if (row.valid_from && row.valid_upto) {
			let valid_from = frappe.datetime.str_to_obj(row.valid_from);
			let valid_upto = frappe.datetime.str_to_obj(row.valid_upto);
			if (valid_upto < valid_from) {
				frappe.msgprint(__('Valid Upto date must be on or after Valid From date.'));
				frappe.model.set_value(cdt, cdn, 'valid_upto', '');
			}
		}

		// Warn if valid_upto is in the past
		if (row.valid_upto) {
			let valid_upto = frappe.datetime.str_to_obj(row.valid_upto);
			let today = frappe.datetime.now_date(true);
			if (valid_upto < today) {
				frappe.msgprint(__('Warning: This permission has already expired on {0}.', [frappe.datetime.str_to_user(row.valid_upto)]));
			}
		}
	}
});

