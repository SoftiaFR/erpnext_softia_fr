frappe.provide("frappe.ui.form");
frappe.ui.form.AssetValueAdjustmentQuickEntryForm = class AssetValueAdjustmentQuickEntryForm extends frappe.ui.form.QuickEntryForm {
    constructor(doctype, after_insert, init_callback, doc, force) {
        super(doctype, after_insert, init_callback, doc, force);
        this.skip_redirect_on_error = true;
    }
    render_dialog() {
        super.render_dialog();

        if (this.doctype === 'Asset Value Adjustment') {
            if (window.frappe && frappe.boot && frappe.boot.lang === 'fr') {
                const wrapper = (this.dialog && this.dialog.$wrapper && this.dialog.$wrapper.length) ? this.dialog.$wrapper[0] : document;
                applyMaleTitleFix("Ajustement de la valeur de l'actif", wrapper);
            }
        }
    }
    make_dialog() {
        super.make_dialog();
    }
};


