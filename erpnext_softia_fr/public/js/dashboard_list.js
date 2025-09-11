frappe.listview_settings['Dashboard'] = {
    formatters: {
        dashboard_name: function(value, df, doc) {
            if (frappe.boot.sysdefaults.language === 'fr') {
                return translate_dashboard_value(value);
            }
            return value; 
        },
        name: function(value, df, doc) {
            if (frappe.boot.sysdefaults.language === 'fr') {
                return translate_dashboard_value(value);
            }
            return value; 
        }
    }
};

function translate_dashboard_value(value) {
    const translations = {
        "Project": __("Projet"),
        "Selling": __("Vente"),
        "Stock": __("Inventaire"),
        "Accounts": __("Comptes"),
        "Buying": __("Achat"),
        "Asset": __("Immobilisation"),
        "Manufacturing": __("Production")
    };
    return translations[value] || value; 
}