import frappe

def after_install():
    create_siret_field()
    create_role_if_not_exists("Gestionnaire Global")
    create_custom_permissions("Gestionnaire Global")
    try:
        create_role_profile("Profil Gestionnaire Global", ["Gestionnaire Global"])
    except frappe.UniqueValidationError:
        print("Role Profile 'Profil Gestionnaire Global' already exists, skipping.")
    except Exception as e:
        print(f"Error creating role profile: {e}")
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
            print(f"Champ personnalisé '{field['fieldname']}' existe déjà, on saute.")
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
            print(f"Champ personnalisé '{field['fieldname']}' inséré.")
        except frappe.DuplicateEntryError:
            print(f"⚠️oublon détecté pour '{field['fieldname']}', insertion ignorée.")

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
        print(f"Rôle {role_name} créé.")


def create_custom_permissions(role):
    perms = [
        ("Sales Order", dict(read=1, write=1, create=1, delete=1, submit=1, amend=1, report=1, email=1, print=1, export=1, share=1)),
        ("Quotation", dict(read=1, write=1, create=1, delete=1, submit=1, amend=1, report=1, email=1, print=1, export=1, share=1)),
        ("Lead", dict(read=1, write=1, create=1, delete=1, report=1, email=1, print=1, export=1, share=1)),
        ("Opportunity", dict(read=1, write=1, create=1, delete=1, report=1, email=1, print=1, export=1, share=1)),
        ("Customer", dict(read=1, write=1, create=1, delete=1, report=1, email=1, print=1, export=1, share=1)),
        ("Contact", dict(read=1, write=1, create=1, delete=1, report=1, email=1, print=1, export=1, share=1)),
        ("Sales Invoice", dict(read=1, write=1, create=1, delete=1, submit=1, amend=1, report=1, email=1, print=1, export=1, share=1)),
        ("Journal Entry", dict(read=1, write=1, create=1, delete=1, submit=1, amend=1, report=1, email=1, print=1, export=1, share=1)),
        ("Item", dict(read=1, write=1, create=1, delete=1, report=1, email=1, print=1, export=1)),
        ("Stock Entry", dict(read=1, write=1, create=1, delete=1, submit=1, amend=1, report=1, email=1, print=1, export=1, share=1)),
        ("Delivery Note", dict(read=1, write=1, create=1, delete=1, submit=1, amend=1, report=1, email=1, print=1, export=1, share=1)),
        ("Warehouse", dict(read=1, export=1)),
        ("Project", dict(read=1, write=1, create=1, delete=1, report=1, email=1, print=1, export=1, share=1)),
        ("Task", dict(read=1, write=1, create=1, delete=1, report=1, email=1, print=1, export=1, share=1)),
        ("Timesheet", dict(read=1, write=1, create=1, delete=1, submit=1, amend=1, report=1, email=1, print=1, export=1, share=1)),
        ("User Permission", dict(read=1, report=1)), 
    ]

    for doctype, perm in perms:
        exists = frappe.db.get_value(
            "Custom DocPerm",
            {
                "parent": doctype,
                "role": role,
                "permlevel": 0
            }
        )
        if not exists:
            frappe.get_doc({
                "doctype": "Custom DocPerm",
                "parent": doctype,
                "parenttype": "DocType",
                "parentfield": "permissions",
                "role": role,
                "permlevel": 0,
                **perm
            }).insert()
            print(f"Permission ajoutée pour {doctype}")
        else:
            print(f"Permission déjà existante pour {doctype}")

def create_role_profile(name, roles):
    # Check if role profile already exists
    if frappe.db.exists("Role Profile", name):
        print(f"Role Profile '{name}' already exists, skipping creation.")
        return
    
    # Create new role profile
    doc = frappe.new_doc("Role Profile")
    doc.role_profile = name
    for role in roles:
        doc.append("roles", {"role": role})
    doc.insert()
    print(f"Role Profile '{name}' created successfully.")
