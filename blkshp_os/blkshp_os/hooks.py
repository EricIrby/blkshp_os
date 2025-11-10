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
	},
	{
		"dt": "Feature Toggle",
		"filters": [["feature_key", "in", [
			"core.workspace.access",
			"products.bulk_operations",
			"inventory.audit_workflows",
			"procurement.ottimate_import",
			"analytics.finance_dashboard"
		]]],
	},
	{
		"dt": "Subscription Plan",
		"filters": [["plan_code", "in", ["FOUNDATION"]]],
	},
	{
		"dt": "Module Activation",
		"filters": [["plan", "in", ["Foundation"]]],
	},
]
