frappe.query_reports["Trial Balance for Party"] = {
    filters: [
        {
            fieldname: "company",
            label: __("Company"),
            fieldtype: "Link",
            options: "Company",
            default: frappe.defaults.get_user_default("Company"),
            reqd: 1
        },
        {
            fieldname: "fiscal_year",
            label: __("Fiscal Year"),
            fieldtype: "Link",
            options: "Fiscal Year",
            default: frappe.defaults.get_user_default("fiscal_year"),
            reqd: 1,
            onchange: function() {
                set_fiscal_year_dates(this.value);
            }
        },
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            reqd: 1
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            reqd: 1
        },
        {
            fieldname: "party_type",
            label: __("Party Type"),
            fieldtype: "Select",
            options: ["Shareholder","Customer","Employee", "Supplier"],
            reqd: 1
        },
		{
			fieldname: "party",
			label: __("Party"),
			fieldtype: "Dynamic Link",
			get_options: function () {
				var party_type = frappe.query_report.get_filter_value("party_type");
				var party = frappe.query_report.get_filter_value("party");
				if (party && !party_type) {
					frappe.throw(__("Please select Party Type first"));
				}
				return party_type;
			},
		},
    ],

    onload: function(report) {
        let fiscal_year = frappe.query_reports["Trial Balance for Party"].filters.find(f => f.fieldname === "fiscal_year").default;
        set_fiscal_year_dates(fiscal_year);
    }
};
function set_fiscal_year_dates(fy) {
    if (!fy) return;
    frappe.call({
        method: "frappe.client.get",
        args: {
            doctype: "Fiscal Year",
            name: fy
        },
        callback: function(r) {
            if (r.message) {
                let from_date = r.message.year_start;
                let to_date = r.message.year_end;

                frappe.query_report.set_filter_value('from_date', from_date);
                frappe.query_report.set_filter_value('to_date', to_date);
            }
        }
    });
}
