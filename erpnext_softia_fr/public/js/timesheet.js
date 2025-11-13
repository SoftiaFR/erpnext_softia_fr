frappe.ui.form.on('Timesheet', {
    onload_post_render(frm) {
        if (frm.is_new() && frappe.boot.lang === 'fr') {
            fix_title(frm,"Feuille de temps");
        }
    },
    refresh(frm) {
        if (frm.is_new() && frappe.boot.lang === 'fr') {
            fix_title(frm,"Feuille de temps");
        }
    }
});

