frappe.ui.form.on('Holiday List', {
    onload_post_render(frm) {
        if (frm.is_new() && frappe.boot.lang === 'fr') {
            fix_title(frm,"Liste des jours fériés");
        }
    },
    refresh(frm) {
        if (frm.is_new() && frappe.boot.lang === 'fr') {
            fix_title(frm,"Liste des jours fériés");
        }
    }
});


