// Copyright (c) 2025, Softia ingénierie and contributors
// For license information, please see license.txt


frappe.query_reports["Interim Management Balances"] = {
    onload: function(report) {
        if (!$('#hide-report-footer-style').length) {
            $('head').append(`
                <style id="hide-report-footer-style">
                    .report-footer.text-muted {
                        display: none !important;
                    }
                </style>
            `);
        }
    },
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		}
	],
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.fieldname === "pourcent_ca" && value) {
			value = value + " %";
		}
		return value;
	}
};
