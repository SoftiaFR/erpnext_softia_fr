import frappe, traceback

def add_interim_safe():
    try:
        ws_name = frappe.db.get_value("Workspace", {"label": "Financial Reports"}, "name")
        if not ws_name:
            print("ERREUR: Workspace 'Financial Reports' introuvable.")
            return

        ws = frappe.get_doc("Workspace", ws_name)

        for l in ws.links:
            if l.link_to == "Interim Management Balances":
                return

        idx_other = None
        for i, l in enumerate(ws.links):
            if l.type == "Card Break" and l.label == "Other Reports":
                idx_other = i
                break

        new_link = ws.append("links", {
            "label": "Interim Management Balances",
            "type": "Link",
            "link_type": "Report",
            "link_to": "Interim Management Balances",
            "is_query_report": 1,
            "dependencies": "GL Entry"
        })

        if idx_other is not None:
            ws.links.remove(new_link)
            ws.links.insert(idx_other + 1, new_link)

        ws.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.clear_cache()
        print("--->  'Interim Management Balances' successfully added to'Other Reports'.")

    except Exception:
        print("Error during operation :")
        traceback.print_exc()

def execute():
    add_interim_safe()
