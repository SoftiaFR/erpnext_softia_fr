frappe.ui.form.on('Opportunity', { 
    onload_post_render(frm) {
        if (frm.is_new() && frappe.boot.lang === 'fr') {
            fix_title(frm,"Opportunité");
        }
    },
    refresh: function(frm) {
        if (frm.is_new()) {
            let default_value = frappe.boot.lang === 'fr' ? 'Ventes' : 'Sales';
            
            if (!frm.doc.opportunity_type || 
                (frappe.boot.lang === 'fr' && frm.doc.opportunity_type === 'Sales') ||
                (frappe.boot.lang !== 'fr' && frm.doc.opportunity_type === 'Ventes')) {
                frm.set_value('opportunity_type', default_value);
            }
        }
        if (frm.is_new() && frappe.boot.lang === 'fr') {
            fix_title(frm,"Opportunité");
        }
    }
});