import frappe
from frappe import _

def after_install():
    create_siret_field()
    frappe.db.commit()



def create_siret_field():
    custom_fields = [
        {
            "fieldname": "siret",
            "label": "SIRET",
            "fieldtype": "Data",
            "insert_after": "company_name",
            "dt": "Company",
            "unique": 1,
        },
        {
            "fieldname": "siret_valide",
            "label": "siret_valide",
            "fieldtype": "Check",
            "insert_after": "siret",
            "dt": "Company",
            "hidden": 1,
        }
    ]

    for field in custom_fields:
        if frappe.db.exists("Custom Field", {
            "dt": field["dt"],
            "fieldname": field["fieldname"]
        }):
            print(_("Custom field '{0}' already exists, skipping.").format(field['fieldname']))
            continue

        try:
            frappe.get_doc({
                "doctype": "Custom Field",
                "dt": field.get("dt"),
                "fieldname": field.get("fieldname"),
                "fieldtype": field.get("fieldtype"),
                "label": field.get("label"),
                "insert_after": field.get("insert_after"),
                "unique": field.get("unique", 0),
                "hidden": field.get("hidden", 0),
                "read_only": field.get("read_only", 0),
                "in_list_view": field.get("in_list_view", 0),
                "reqd": field.get("reqd", 0),
                "no_copy": field.get("no_copy", 0),
                "bold": field.get("bold", 0),
                "translatable": field.get("translatable", 0),
                "allow_in_quick_entry": field.get("allow_in_quick_entry", 0),
                "allow_on_submit": field.get("allow_on_submit", 0),
            }).insert()
            print(_("Custom field '{0}' inserted.").format(field['fieldname']))
        except frappe.DuplicateEntryError:
            print(_("Duplicate detected for '{0}', skipping insertion.").format(field['fieldname']))

    frappe.db.commit()

EXCLUDED_DOCTYPES = [
    "User", "Role", "Role Profile", "Has Role", 
    "DocPerm", "Custom DocPerm", "Page", "Module Def", "Deleted Document"
]


def add_permission_if_not_exists(doctype, role):
    exists = frappe.db.get_value(
        "Custom DocPerm",
        {"parent": doctype, "role": role, "permlevel": 0}
    )

    if exists:
        frappe.logger().info(_("Permission already exists for {0}").format(doctype))
        return

    try:
        frappe.get_doc({
            "doctype": "Custom DocPerm",
            "parent": doctype,
            "parenttype": "DocType",
            "parentfield": "permissions",
            "role": role,
            "permlevel": 0,
            "read": 1,
            "select": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
            "submit": 1,
            "amend": 1,
            "report": 1,
            "email": 1,
            "print": 1,
            "export": 1,
            "share": 1
        }).insert()
        frappe.logger().info(_("Permission added for {0}").format(doctype))
    except Exception as e:
        frappe.logger().error(_("Error while adding permission to {0}: {1}").format(doctype, e))
