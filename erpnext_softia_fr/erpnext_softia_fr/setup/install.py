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
        }
    ]

    for field in custom_fields:
        if not frappe.db.exists("Custom Field", f"{field['dt']}-{field['fieldname']}"):
            frappe.get_doc({
                "doctype": "Custom Field",
                "dt": field["dt"],
                "fieldname": field["fieldname"],
                "fieldtype": field["fieldtype"],
                "label": field["label"],
                "insert_after": field.get("insert_after", ""),
                "unique": field.get("unique", 0),
            }).insert()
    
    frappe.db.commit()
    print("Champ personnalisé 'SIRET' ajouté au Doctype Company.")

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
        frappe.msgprint(f"Rôle {role_name} créé.")


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
        if not frappe.db.exists({
            "doctype": "Custom DocPerm",
            "parent": doctype,
            "role": role,
            "permlevel": 0
        }):
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
