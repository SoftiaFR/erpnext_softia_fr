frappe.ui.form.on('Notification', {
    onload_post_render(frm) {
        if (frm.is_new() && frappe.boot.lang === 'fr') {
            fix_title(frm,"Notification");
        }
    },
    refresh(frm) {
        if (frm.is_new() && frappe.boot.lang === 'fr') {
            fix_title(frm,"Notification");
        }
    }
});


