frappe.ui.form.on('Company', {
    siret: function(frm) {
        const siret = frm.doc.siret;
        frm.fields_dict["siret"].$wrapper.find(".siret-message").remove();

        if (!siret) return;

        if (!/^\d{14}$/.test(siret)) {
            frm.set_value("siret_valide", 0);
            frm.fields_dict["siret"].$wrapper.append(
                `<div class="text-danger small mt-1 siret-message">⚠️ ${__("The SIRET number must be exactly 14 digits.")}</div>`
            );
            return;
        }

        frappe.call({
            method: "erpnext_softia_fr.api.siret.verifier_siret",
            args: { siret },
            freeze: true,
            freeze_message: __("Checking SIRET..."),
            callback: function(r) {
                if (r.message.status === "success") {
                    const data = r.message.data;
                    frm.set_value("company_name", data.denomination);
                    frm.set_value("country", "France");
                    frm.set_value("siret_valide", 1); 
                    frm.fields_dict["siret"].$wrapper.append(
                        `<div class="text-success small mt-1 siret-message">✅ ${__("SIRET recognized")}: ${data.denomination}</div>`
                    );
                } else {
                    frm.set_value("siret_valide", 0); 
                    frm.fields_dict["siret"].$wrapper.append(
                        `<div class="text-danger small mt-1 siret-message">❌ ${__(r.message.message)}</div>`
                    );
                }
            }
        });
    },

    validate: function(frm) {
        if (!frm.doc.siret_valide) {
            frappe.throw(__("The SIRET number is invalid or has not been verified."));
        }
    }
});
