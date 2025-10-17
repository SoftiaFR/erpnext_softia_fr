import frappe

def translation_stock_entry_type(args=None):
    system_lang = frappe.db.get_single_value("System Settings", "language") or "en"

    if not system_lang.startswith("fr"):
        return


    translations = {
        "Material Issue": "Sortie de Matériel",
        "Material Receipt": "Réception de matériel",
        "Material Transfer": "Transfert de matériel",
        "Manufacture": "Fabriquer",
        "Repack": "Reconditionner",
        "Disassemble": "Désassembler",
        "Send to Subcontractor": "Envoyer au Sous-traitant",
        "Material Transfer for Manufacture": "Transfert de Matériel pour Fabrication",
        "Material Consumption for Manufacture": "Consommation de Matériel pour Fabrication"
    }

    for eng, fr in translations.items():
        if frappe.db.exists("Stock Entry Type", eng):
            try:
                frappe.rename_doc("Stock Entry Type", eng, fr, force=True)
                frappe.db.set_value("Stock Entry Type", fr, "purpose", fr)
                frappe.db.set_value("Stock Entry Type", fr, "is_standard", 1)
                frappe.logger().info(f"{eng} → {fr}")
            except Exception as e:
                frappe.logger().warning(f" Error during translation of {eng} : {e}")

    frappe.db.commit()
