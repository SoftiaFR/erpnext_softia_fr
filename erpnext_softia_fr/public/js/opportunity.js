frappe.ui.form.on('Opportunity', { 
    refresh: function(frm) {
        if (frm.is_new()) {
            let default_value = frappe.boot.lang === 'fr' ? 'Ventes' : 'Sales';
            
            if (!frm.doc.opportunity_type || 
                (frappe.boot.lang === 'fr' && frm.doc.opportunity_type === 'Sales') ||
                (frappe.boot.lang !== 'fr' && frm.doc.opportunity_type === 'Ventes')) {
                frm.set_value('opportunity_type', default_value);
            }
        }
    }
});