/**
 * Subscription Management Page
 *
 * BLKSHP Operations interface for managing tenant subscriptions.
 * Allows viewing and modifying subscription plans and module activations.
 *
 * @restricted BLKSHP Operations, System Manager
 */

frappe.pages['subscription-management'].on_page_load = function(wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __('Subscription Management'),
		single_column: true
	});

	// Add descriptive text
	page.add_inner_message(__('Manage tenant subscriptions, plans, and module activations. This tool is for BLKSHP Operations staff only.'));

	// Add refresh button
	page.set_secondary_action(__('Refresh'), () => {
		load_tenants(page);
	}, 'refresh');

	// Store page reference
	wrapper.subscription_management = {
		page: page,
		load: () => load_tenants(page)
	};

	// Initial load
	load_tenants(page);
};

/**
 * Load and display all tenants
 */
function load_tenants(page) {
	frappe.call({
		method: 'blkshp_os.blkshp_os.core_platform.page.subscription_management.subscription_management.get_all_tenants',
		callback: function(r) {
			if (r.message) {
				render_tenants_table(page, r.message);
			}
		}
	});
}

/**
 * Render the tenants table
 */
function render_tenants_table(page, tenants) {
	const $content = $(page.body).find('.main-section');
	$content.empty();

	// Show summary stats
	const total_tenants = tenants.length;
	const tenants_with_plans = tenants.filter(t => t.plan_code).length;
	const tenants_without_plans = total_tenants - tenants_with_plans;

	$content.append(`
		<div class="subscription-stats" style="margin-bottom: 20px; display: flex; gap: 20px;">
			<div class="stat-card" style="flex: 1; padding: 15px; background: var(--bg-light-gray); border-radius: 8px;">
				<div class="stat-value" style="font-size: 24px; font-weight: bold;">${total_tenants}</div>
				<div class="stat-label" style="color: var(--text-muted);">Total Tenants</div>
			</div>
			<div class="stat-card" style="flex: 1; padding: 15px; background: var(--bg-light-gray); border-radius: 8px;">
				<div class="stat-value" style="font-size: 24px; font-weight: bold; color: var(--green-500);">${tenants_with_plans}</div>
				<div class="stat-label" style="color: var(--text-muted);">With Plans</div>
			</div>
			<div class="stat-card" style="flex: 1; padding: 15px; background: var(--bg-light-gray); border-radius: 8px;">
				<div class="stat-value" style="font-size: 24px; font-weight: bold; color: var(--orange-500);">${tenants_without_plans}</div>
				<div class="stat-label" style="color: var(--text-muted);">Without Plans</div>
			</div>
		</div>
	`);

	if (tenants.length === 0) {
		$content.append(`
			<div class="empty-state" style="text-align: center; padding: 40px; color: var(--text-muted);">
				<p>${__('No tenants found')}</p>
			</div>
		`);
		return;
	}

	// Create table
	const $table = $(`
		<table class="table table-bordered tenants-table" style="width: 100%; margin-top: 10px;">
			<thead>
				<tr style="background: var(--bg-light-gray);">
					<th style="width: 25%;">${__('Company')}</th>
					<th style="width: 20%;">${__('Subscription Plan')}</th>
					<th style="width: 15%;">${__('Billing')}</th>
					<th style="width: 20%;">${__('Modules')}</th>
					<th style="width: 20%;">${__('Actions')}</th>
				</tr>
			</thead>
			<tbody></tbody>
		</table>
	`);

	const $tbody = $table.find('tbody');

	tenants.forEach(tenant => {
		const plan_badge = tenant.plan_code
			? `<span class="badge badge-success">${tenant.plan_name || tenant.plan_code}</span>`
			: `<span class="badge badge-warning">${__('No Plan')}</span>`;

		const billing_info = tenant.billing_frequency
			? `${tenant.billing_frequency}${tenant.base_price ? ` - ${frappe.format(tenant.base_price, {fieldtype: 'Currency'})}` : ''}`
			: '-';

		const module_info = tenant.module_count > 0
			? `${tenant.module_count} ${__('enabled')}`
			: __('None');

		const $row = $(`
			<tr data-company="${frappe.utils.escape_html(tenant.company)}">
				<td>
					<strong>${frappe.utils.escape_html(tenant.company_name)}</strong><br>
					<small class="text-muted">${frappe.utils.escape_html(tenant.company)} (${frappe.utils.escape_html(tenant.abbr)})</small>
				</td>
				<td>${plan_badge}</td>
				<td><small>${billing_info}</small></td>
				<td>
					<small>${module_info}</small>
					${tenant.has_overrides ? '<br><span class="badge badge-info" style="font-size: 9px;">Overrides</span>' : ''}
				</td>
				<td>
					<button class="btn btn-xs btn-default btn-view-details" style="margin-right: 5px;">
						<i class="fa fa-eye"></i> ${__('Details')}
					</button>
					<button class="btn btn-xs btn-primary btn-change-plan">
						<i class="fa fa-edit"></i> ${__('Change Plan')}
					</button>
				</td>
			</tr>
		`);

		// Bind event handlers
		$row.find('.btn-view-details').on('click', () => {
			show_tenant_details(page, tenant.company);
		});

		$row.find('.btn-change-plan').on('click', () => {
			show_change_plan_dialog(page, tenant.company, tenant.plan_code);
		});

		$tbody.append($row);
	});

	$content.append($table);
}

/**
 * Show detailed view of a tenant
 */
function show_tenant_details(page, company) {
	frappe.call({
		method: 'blkshp_os.blkshp_os.core_platform.page.subscription_management.subscription_management.get_tenant_details',
		args: { company: company },
		callback: function(r) {
			if (r.message) {
				render_tenant_details_dialog(page, company, r.message);
			}
		}
	});
}

/**
 * Render tenant details in a dialog
 */
function render_tenant_details_dialog(page, company, details) {
	const dialog = new frappe.ui.Dialog({
		title: __('Tenant Details: {0}', [company]),
		size: 'large',
		fields: [
			{
				fieldtype: 'HTML',
				fieldname: 'details_html'
			}
		]
	});

	// Build HTML content
	let html = '<div class="tenant-details">';

	// Current plan section
	html += '<h5 style="margin-top: 0;">Current Plan</h5>';
	if (details.current_plan) {
		html += `
			<table class="table table-bordered" style="margin-bottom: 20px;">
				<tr>
					<th style="width: 30%;">Plan Code</th>
					<td>${frappe.utils.escape_html(details.current_plan.code)}</td>
				</tr>
				<tr>
					<th>Plan Name</th>
					<td>${frappe.utils.escape_html(details.current_plan.name)}</td>
				</tr>
				<tr>
					<th>Billing</th>
					<td>${details.current_plan.billing_frequency || '-'}</td>
				</tr>
				<tr>
					<th>Base Price</th>
					<td>${details.current_plan.base_price ? frappe.format(details.current_plan.base_price, {fieldtype: 'Currency'}) : '-'}</td>
				</tr>
			</table>
		`;
	} else {
		html += '<p class="text-muted">No plan assigned</p>';
	}

	// Modules section
	html += '<h5>Modules</h5>';
	if (details.modules && details.modules.length > 0) {
		html += '<table class="table table-bordered" style="margin-bottom: 20px;"><thead><tr><th>Module</th><th>Status</th><th>Actions</th></tr></thead><tbody>';
		details.modules.forEach(module => {
			const status_badge = module.is_enabled
				? '<span class="badge badge-success">Enabled</span>'
				: '<span class="badge badge-secondary">Disabled</span>';

			const required_badge = module.is_required
				? '<span class="badge badge-info" style="margin-left: 5px;">Required</span>'
				: '';

			const toggle_btn = !module.is_required
				? `<button class="btn btn-xs btn-default btn-toggle-module"
						data-company="${frappe.utils.escape_html(company)}"
						data-module="${frappe.utils.escape_html(module.key)}"
						data-enabled="${!module.is_enabled}">
						${module.is_enabled ? __('Disable') : __('Enable')}
					</button>`
				: '<small class="text-muted">Required</small>';

			html += `
				<tr>
					<td><strong>${frappe.utils.escape_html(module.label)}</strong><br><small class="text-muted">${frappe.utils.escape_html(module.key)}</small></td>
					<td>${status_badge}${required_badge}</td>
					<td>${toggle_btn}</td>
				</tr>
			`;
		});
		html += '</tbody></table>';
	} else {
		html += '<p class="text-muted">No modules defined</p>';
	}

	html += '</div>';

	dialog.fields_dict.details_html.$wrapper.html(html);

	// Bind toggle buttons
	dialog.fields_dict.details_html.$wrapper.find('.btn-toggle-module').on('click', function() {
		const $btn = $(this);
		const module_key = $btn.data('module');
		const enabled = $btn.data('enabled');

		show_toggle_module_dialog(page, company, module_key, enabled, () => {
			dialog.hide();
		});
	});

	dialog.show();
}

/**
 * Show dialog to change tenant plan
 */
function show_change_plan_dialog(page, company, current_plan) {
	// Get available plans
	frappe.call({
		method: 'blkshp_os.blkshp_os.core_platform.page.subscription_management.subscription_management.get_tenant_details',
		args: { company: company },
		callback: function(r) {
			if (r.message && r.message.available_plans) {
				const plans = r.message.available_plans;

				const dialog = new frappe.ui.Dialog({
					title: __('Change Subscription Plan for {0}', [company]),
					fields: [
						{
							fieldtype: 'Select',
							fieldname: 'new_plan',
							label: __('New Plan'),
							options: plans.map(p => p.name),
							default: current_plan,
							reqd: 1
						},
						{
							fieldtype: 'Small Text',
							fieldname: 'reason',
							label: __('Reason for Change'),
							description: __('This will be logged for audit purposes'),
							reqd: 1
						}
					],
					primary_action_label: __('Change Plan'),
					primary_action: function(values) {
						frappe.call({
							method: 'blkshp_os.blkshp_os.core_platform.page.subscription_management.subscription_management.change_tenant_plan',
							args: {
								company: company,
								new_plan: values.new_plan,
								reason: values.reason
							},
							callback: function(r) {
								if (r.message && r.message.success) {
									frappe.show_alert({
										message: r.message.message,
										indicator: 'green'
									});
									dialog.hide();
									load_tenants(page);
								}
							}
						});
					}
				});

				dialog.show();
			}
		}
	});
}

/**
 * Show dialog to toggle module
 */
function show_toggle_module_dialog(page, company, module_key, enabled, callback) {
	const action = enabled ? __('Enable') : __('Disable');

	const dialog = new frappe.ui.Dialog({
		title: __(`{0} Module: {1}`, [action, module_key]),
		fields: [
			{
				fieldtype: 'HTML',
				fieldname: 'warning_html',
				options: `<p>${__('You are about to {0} the <strong>{1}</strong> module for {2}.',
					[action.toLowerCase(), module_key, company])}</p>`
			},
			{
				fieldtype: 'Small Text',
				fieldname: 'reason',
				label: __('Reason'),
				description: __('This will be logged for audit purposes'),
				reqd: 1
			}
		],
		primary_action_label: action,
		primary_action: function(values) {
			frappe.call({
				method: 'blkshp_os.blkshp_os.core_platform.page.subscription_management.subscription_management.toggle_module',
				args: {
					company: company,
					module_key: module_key,
					enabled: enabled,
					reason: values.reason
				},
				callback: function(r) {
					if (r.message && r.message.success) {
						frappe.show_alert({
							message: r.message.message,
							indicator: 'green'
						});
						dialog.hide();
						if (callback) callback();
						load_tenants(page);
					}
				}
			});
		}
	});

	dialog.show();
}
