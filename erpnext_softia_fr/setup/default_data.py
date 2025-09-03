import frappe
from frappe import _

def create_data(args):
    system_language = frappe.db.get_single_value("System Settings", "language")

    create_custom_payment_modes(system_language)
    create_supplier_group(system_language)

def create_custom_payment_modes(system_language):
    """Create a custom payment method if it does not already exist"""

    # Apply language context for translations
    frappe.local.lang = system_language or "en"
    frappe.local.language = system_language

    mode_name = _("SEPA Direct Debit", lang=system_language)
    
    if not frappe.db.exists("Mode of Payment", mode_name):
        mode = frappe.get_doc({
            "doctype": "Mode of Payment",
            "mode_of_payment": mode_name,
            "enabled": 1,
            "type": "Bank"  # "Cash", "Bank", "General"
        })
        mode.insert(ignore_permissions=True)
        frappe.db.commit()


def create_supplier_group(system_language):
    """Create the supplier group 'Consumables'"""
    # Apply language context for translations
    frappe.local.lang = system_language
    frappe.local.language = system_language

    group_name = _("Consumables")

    if not frappe.db.exists("Supplier Group", group_name):
        doc = frappe.get_doc({
            "doctype": "Supplier Group",
            "supplier_group_name": group_name,
            "parent_supplier_group": _("All Supplier Groups", lang=system_language),
            "is_group": 0,
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        frappe.logger().info(f"✅ Supplier Group created : {group_name}")
    else:
        frappe.logger().info(f"ℹ️ Already existing Supplier Group: {group_name}")

