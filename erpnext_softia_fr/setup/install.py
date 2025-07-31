import frappe
from frappe import _
from frappe.model.document import Document

def after_install():
    create_siret_field()
    create_role_if_not_exists("Gestionnaire Global")
    create_custom_permissions_for_modules("Gestionnaire Global")
    restrict_unwanted_workspaces()
    restrict_workspaces_to_role("Gestionnaire Global")
    hide_unwanted_workspaces()
    grant_report_access("Gestionnaire Global")
    grant_all_module_reports_access("Gestionnaire Global")

    try:
        create_role_profile("Profil Gestionnaire Global", ["Gestionnaire Global"])
    except frappe.UniqueValidationError:
        print(_("Role Profile 'Profil Gestionnaire Global' already exists, skipping."))
    except Exception as e:
        print(_("Error creating role profile: {0}").format(e))

    create_login_gestionnaire_doctype()
    create_login_gestionnaire_webform()

    frappe.db.commit()


def grant_report_access(role):
    from frappe.core.doctype.report.report import Report  # type: ignore

    if frappe.db.exists("Report", "General Ledger"):
        doc = frappe.get_doc("Report", "General Ledger")
        if role not in [r.role for r in doc.roles]:
            doc.append("roles", {"role": role})
            doc.save()
            frappe.msgprint(_("✅ Access to the 'General Ledger' report has been granted to role: {0}.").format(role))
        else:
            frappe.msgprint(_("🔸 The role '{0}' already has access to the 'General Ledger' report.").format(role))
    else:
        frappe.msgprint(_("❌ Report 'General Ledger' not found."))



def hide_unwanted_workspaces():
    allowed_modules = ["Accounts", "Selling", "Stock", "Projects", "CRM", "Manufacturing", "Setup"]
    always_visible_workspaces = ["Home"]

    workspaces = frappe.get_all("Workspace", fields=["name", "module"])

    for ws in workspaces:
        try:
            doc = frappe.get_doc("Workspace", ws.name)

            if ws.name in always_visible_workspaces or ws.module in allowed_modules:
                doc.is_hidden = 0
                doc.save()
                print(_("Workspace '{0}' is visible").format(ws.name))
            else:
                doc.is_hidden = 1
                doc.save()
                print(_("Workspace '{0}' hidden via is_hidden").format(ws.name))

        except Exception as e:
            print(_("Error processing workspace {0}: {1}").format(ws.name, e))

def restrict_unwanted_workspaces():
    allowed_modules = ["Accounts", "Selling", "Stock", "Projects", "CRM", "Manufacturing", "Setup"]
    always_allowed_workspaces = ["Home"]
    hidden_role = "__Masqué__"

    workspaces = frappe.get_all("Workspace", fields=["name", "module"])

    for ws in workspaces:
        try:
            doc = frappe.get_doc("Workspace", ws.name)

            if ws.name in always_allowed_workspaces or ws.module in allowed_modules:
                print(_("Workspace '{0}' retained").format(ws.name))
            else:
                doc.restrict_to_role = [hidden_role]
                doc.save()
                print(_("Workspace '{0}' restricted from users").format(ws.name))

        except Exception as e:
            print(_("Error with workspace {0}: {1}").format(ws.name, e))



def restrict_workspaces_to_role(role_name):
    allowed_modules = ["Accounts", "Selling", "Stock", "CRM", "Projects", "Manufacturing", "Setup"]
    workspaces = frappe.get_all("Workspace", filters={"module": ["not in", allowed_modules]})
    
    for ws in workspaces:
        try:
            doc = frappe.get_doc("Workspace", ws.name)

            def is_valid_link(link):
                return frappe.db.exists("DocType", link.get("link_to")) if link.get("link_to") else True

            if hasattr(doc, "cards"):
                doc.cards = [card for card in doc.cards if is_valid_link(card)]
            if hasattr(doc, "links"):
                doc.links = [l for l in doc.links if is_valid_link(l)]
            if hasattr(doc, "onboarding_items"):
                doc.onboarding_items = [i for i in doc.onboarding_items if is_valid_link(i)]
            if hasattr(doc, "shortcuts"):
                doc.shortcuts = [s for s in doc.shortcuts if is_valid_link(s)]

            doc.restrict_to_role = [role_name]
            doc.save()
            print(_("Workspace '{0}' restricted to role {1}").format(ws.name, role_name))

        except Exception as e:
            print(_("Error modifying workspace {0}: {1}").format(ws.name, e))



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


def create_role_if_not_exists(role_name):
    if not frappe.db.exists("Role", role_name):
        frappe.get_doc({
            "doctype": "Role",
            "role_name": role_name,
            "desk_access": 1,
            "is_custom": 1,
            "disabled": 0,
            "restrict_to_domain": None,
        }).insert()
        print(_("Role {0} created.").format(role_name))


def create_role_profile(name, roles):
    if frappe.db.exists("Role Profile", name):
        print(_("Role Profile '{0}' already exists, skipping creation.").format(name))
        return
    
    doc = frappe.new_doc("Role Profile")
    doc.role_profile = name
    for role in roles:
        doc.append("roles", {"role": role})
    doc.insert()
    print(_("Role Profile '{0}' created successfully.").format(name))

EXCLUDED_DOCTYPES = [
    "User", "Role", "Role Profile", "Has Role", 
    "DocPerm", "Custom DocPerm", "Page", "Module Def", "Deleted Document"
]

def create_custom_permissions_for_modules(role):
    target_modules = ["Accounts", "Selling", "Stock", "Projects", "CRM", "Manufacturing", "Setup", "Geo"]
    additional_doctypes = ["Supplier", "UOM", "Supplier Group", "Purchase Order", "Currency", "Company", "UOM"]

    for module in target_modules:
        doctypes = frappe.get_all("DocType", filters={"module": module}, pluck="name")

        for doctype in doctypes:
            if doctype in EXCLUDED_DOCTYPES:
                continue
            add_permission_if_not_exists(doctype, role)

    for doctype in additional_doctypes:
        if doctype in EXCLUDED_DOCTYPES:
            continue
        add_permission_if_not_exists(doctype, role)


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


def grant_all_module_reports_access(role="Gestionnaire Global"):
    modules = ["Accounts", "Selling", "Stock", "Projects", "CRM", "Manufacturing", "Setup"]
    total_updated = 0
    total_skipped = 0

    for module in modules:
        reports = frappe.get_all("Report", filters={"module": module}, pluck="name")
        print(_("Processing {0} report(s) from module '{1}'").format(len(reports), module))

        for report_name in reports:
            try:
                doc = frappe.get_doc("Report", report_name)

                if doc.letter_head and not frappe.db.exists("Letter Head", doc.letter_head):
                    frappe.logger().warning(_("Report '{0}' refers to missing Letter Head: '{1}', clearing...").format(report_name, doc.letter_head))
                    doc.letter_head = None

                if role not in [r.role for r in doc.roles]:
                    doc.append("roles", {"role": role})
                    doc.save()
                    print(_("Access granted to report: {0}").format(report_name))
                    total_updated += 1
                else:
                    print(_("Role already has access to report: {0}").format(report_name))

            except Exception as e:
                frappe.logger().error(_("Could not process report '{0}': {1}").format(report_name, e))
                total_skipped += 1

    frappe.db.commit()
    print(_("Done: {0} report(s) updated, {1} skipped due to errors.").format(total_updated, total_skipped))

def create_login_gestionnaire_doctype():
    if frappe.db.exists("DocType", "Login Gestionnaire"):
        print("Doctype 'Login Gestionnaire' already exists, skipping.")
        return
    doc = frappe.new_doc("DocType")
    doc.name = "Login Gestionnaire"
    doc.module = "erpnext_softia_fr"
    doc.custom = 0
    doc.autoname = "field:email"
    doc.is_submittable = 0
    doc.istable = 0
    doc.has_web_view = 0
    doc.allow_guest_to_view = 0
    
    doc.append("permissions", {
        "role": "Guest",
        "read": 1,
        "write": 1,
        "create": 1,
        "delete": 0,
        "submit": 0,
        "cancel": 0,
        "amend": 0
    })
   
    doc.append("permissions", {
        "role": "System Manager",
        "read": 1,
        "write": 1,
        "create": 1,
        "delete": 1,
        "submit": 0,
        "cancel": 0,
        "amend": 0
    })
    
    fields = [
        {
            "label": "Nom complet",
            "fieldname": "full_name",
            "fieldtype": "Data",
            "reqd": 1,
            "in_list_view": 1
        },
        {
            "label": "Email",
            "fieldname": "email",
            "fieldtype": "Data",
            "reqd": 1,
            "unique": 1,
            "in_list_view": 1
        },
        {
            "label": "Date de création",
            "fieldname": "creation_date",
            "fieldtype": "Datetime",
            "read_only": 1,
            "in_list_view": 1
        }
    ]
   
    for field in fields:
        doc.append("fields", field)
    doc.insert()
    frappe.db.commit()
    print("Doctype 'Login Gestionnaire' created without password field.")

def create_login_gestionnaire_webform():
    if frappe.db.exists("Web Form", "Login Gestionnaire"):
        print("Web Form 'Login Gestionnaire' already exists, skipping.")
        return
    webform = frappe.new_doc("Web Form")
    webform.name = "login_gestionnaire"
    webform.title = "Inscrivez-vous"
    webform.route = "signup-gestionnaire"
    webform.doc_type = "Login Gestionnaire"
    webform.allow_guest = 1
    webform.is_standard = 0
    webform.module = "erpnext_softia_fr"
   
    webform.published = 1  
   
    webform.success_title = "Compte créé avec succès"
    webform.success_message = """
        Votre compte a été créé avec succès ! 
        Vous pouvez maintenant vous connecter.
    """
    webform.success_url = ""
    webform.web_form_fields = []

    fields_data = [
        {
            "fieldname": "full_name",
            "label": "Nom complet",
            "fieldtype": "Data",
            "reqd": 1,
            "description": "Entrez votre nom complet"
        },
        {
            "fieldname": "email",
            "label": "Adresse email",
            "fieldtype": "Data",
            "reqd": 1,
            "unique": 1,
            "description": "Cette adresse sera utilisée pour vous connecter et recevoir vos identifiants"
        }
    ]
    
    for f in fields_data:
        child = frappe.new_doc("Web Form Field")
        for k, v in f.items():
            setattr(child, k, v)
        webform.append("web_form_fields", child)
    webform.insert()
    frappe.db.commit()
    print("Web Form 'Login Gestionnaire' created without password field.")