import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def remove_custom_fields():
    for fieldname in ["super_parent"]:
        if frappe.db.exists("Custom Field", {"dt": "Account", "fieldname": fieldname}):
            frappe.delete_doc("Custom Field", frappe.db.get_value("Custom Field", {"dt": "Account", "fieldname": fieldname}, "name"))


def add_custom_fields():
    if not frappe.db.exists("Custom Field", {"dt": "Account", "fieldname": "super_parent"}):
        create_custom_field("Account", {
            "fieldname": "super_parent",
            "label": "Accounting Class",
            "fieldtype": "Link",
            "options": "Account",  
            "insert_after": "parent_account",  
            "read_only": 1
        })

def execute():
    remove_custom_fields()
    add_custom_fields()
