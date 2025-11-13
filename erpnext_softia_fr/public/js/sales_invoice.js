frappe.ui.form.on('Sales Invoice', {
    onload_post_render(frm) {
        if (frm.is_new() && frappe.boot.lang === 'fr') {
            fix_title(frm,"Facture de vente");
        }
    },
    refresh(frm) {
        if (frm.is_new() && frappe.boot.lang === 'fr') {
            fix_title(frm,"Facture de vente");
        }
    }
});


