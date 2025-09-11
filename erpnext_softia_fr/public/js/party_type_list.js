frappe.listview_settings['Party Type'] = {
    formatters: {
        name: function(value, df, doc) {
            if (frappe.boot.sysdefaults.language === 'fr') {
                return translate_party_type_value(value);
            }
            return value; 
        }
    }
};

function translate_party_type_value(value) {
    const translations = {
        "Shareholder": __("Associé"),
        "Customer": __("Client"),
        "Employee": __("Salarié"),
        "Supplier": __("Fournisseur")
    };
    return translations[value] || value; 
}
