frappe.ui.form.on('Quality Procedure', {
    onload_post_render(frm) {
        if (frm.is_new() && frappe.boot.lang === 'fr') {
            fix_title(frm,"Procédure qualité");
        }
    },
    refresh(frm) {
        if (frm.is_new() && frappe.boot.lang === 'fr') {
            fix_title(frm,"Procédure qualité");
        }
    }
});


