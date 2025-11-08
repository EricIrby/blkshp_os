// Role DocType client script
frappe.ui.form.on('Role', {
	refresh: function(frm) {
		// Add custom buttons for role management
		if (!frm.is_new()) {
			// Add button to view users with this role
			frm.add_custom_button(__('View Users'), function() {
				frappe.set_route('List', 'User', {
					'roles.role': frm.doc.name
				});
			}, __('View'));

			// Add button to view role summary
			frm.add_custom_button(__('Role Summary'), function() {
				frappe.call({
					method: 'blkshp_os.permissions.roles.get_role_summary',
					args: {
						role: frm.doc.name
					},
					callback: function(r) {
						if (r.message) {
							let summary = r.message;
							let html = `
								<div class="role-summary">
									<h4>${__('Role Summary')}</h4>
									<table class="table table-bordered">
										<tr>
											<th>${__('Users with Role')}</th>
											<td>${summary.user_count}</td>
										</tr>
										<tr>
											<th>${__('Total Permissions')}</th>
											<td>${summary.permission_count}</td>
										</tr>
										<tr>
											<th>${__('Custom Role')}</th>
											<td>${summary.is_custom ? __('Yes') : __('No')}</td>
										</tr>
									</table>
									<h5>${__('Permissions by Category')}</h5>
									<table class="table table-bordered">
										${Object.entries(summary.permissions_by_category || {})
											.map(([cat, count]) => `<tr><td>${cat}</td><td>${count}</td></tr>`)
											.join('')}
									</table>
								</div>
							`;
							frappe.msgprint({
								title: __('Role Summary: {0}', [frm.doc.name]),
								message: html,
								indicator: 'blue',
								wide: true
							});
						}
					}
				});
			}, __('View'));

			// Add button to bulk add permissions
			frm.add_custom_button(__('Add Permissions'), function() {
				frappe.call({
					method: 'blkshp_os.api.roles.get_available_permissions',
					callback: function(r) {
						if (r.message) {
							let permissions = r.message;
							let existing_codes = frm.doc.custom_permissions.map(p => p.permission_code);
							
							// Filter out already granted permissions
							let available = permissions.filter(p => !existing_codes.includes(p.code));
							
							if (available.length === 0) {
								frappe.msgprint(__('All permissions are already granted to this role.'));
								return;
							}

							// Group by category
							let by_category = {};
							available.forEach(p => {
								if (!by_category[p.category]) {
									by_category[p.category] = [];
								}
								by_category[p.category].push(p);
							});

							// Create dialog
							let d = new frappe.ui.Dialog({
								title: __('Add Permissions'),
								fields: [
									{
										fieldtype: 'HTML',
										fieldname: 'permissions_html'
									}
								],
								primary_action_label: __('Add Selected'),
								primary_action: function() {
									let selected = [];
									d.$wrapper.find('input[type="checkbox"]:checked').each(function() {
										selected.push($(this).val());
									});

									if (selected.length === 0) {
										frappe.msgprint(__('Please select at least one permission.'));
										return;
									}

									// Add permissions to child table
									selected.forEach(code => {
										frm.add_child('custom_permissions', {
											permission_code: code,
											is_granted: 1
										});
									});

									frm.refresh_field('custom_permissions');
									d.hide();
									frappe.show_alert({
										message: __('Added {0} permission(s)', [selected.length]),
										indicator: 'green'
									});
								}
							});

							// Build HTML
							let html = '<div class="permission-selector">';
							Object.keys(by_category).sort().forEach(category => {
								html += `<h5>${category}</h5><div class="permission-category">`;
								by_category[category].forEach(perm => {
									html += `
										<div class="checkbox">
											<label>
												<input type="checkbox" value="${perm.code}">
												<strong>${perm.name}</strong>
												${perm.department_restricted ? '<span class="label label-info">Dept</span>' : ''}
												<br>
												<small class="text-muted">${perm.description}</small>
											</label>
										</div>
									`;
								});
								html += '</div>';
							});
							html += '</div>';

							d.fields_dict.permissions_html.$wrapper.html(html);
							d.show();
						}
					}
				});
			}, __('Actions'));
		}

		// Set indicator for custom roles
		if (frm.doc.is_custom_role) {
			frm.dashboard.set_headline_alert(__('Custom Role'), 'blue');
		}
	},

	is_custom_role: function(frm) {
		if (frm.doc.is_custom_role && !frm.doc.role_description) {
			frappe.msgprint(__('Please add a description for this custom role.'));
		}
	}
});

// Role Permission child table handlers
frappe.ui.form.on('Role Permission', {
	permission_code: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		
		// Auto-populate permission details
		if (row.permission_code) {
			frappe.call({
				method: 'blkshp_os.permissions.constants.get_permission',
				args: {
					code: row.permission_code
				},
				callback: function(r) {
					if (r.message) {
						let perm = r.message;
						frappe.model.set_value(cdt, cdn, 'permission_name', perm.name);
						frappe.model.set_value(cdt, cdn, 'permission_category', perm.category);
						frappe.model.set_value(cdt, cdn, 'description', perm.description);
						frappe.model.set_value(cdt, cdn, 'department_restricted', perm.department_restricted);
					}
				}
			});
		}
	},

	custom_permissions_add: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		// Set default to granted
		frappe.model.set_value(cdt, cdn, 'is_granted', 1);
	}
});

