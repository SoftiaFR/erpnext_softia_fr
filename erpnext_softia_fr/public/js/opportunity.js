frappe.ui.form.on('Opportunity', {
    setup: function(frm) {
        frm.set_df_property('opportunity_type', 'default', 'Ventes');
    },
    
    refresh: function(frm) {
        if (frm.is_new()) {
            if (!frm.doc.opportunity_type || frm.doc.opportunity_type === 'Sales') {
                frm.set_value('opportunity_type', 'Ventes');
            }
        }
    }
});