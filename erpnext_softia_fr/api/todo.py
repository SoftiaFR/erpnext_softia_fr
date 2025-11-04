import frappe

@frappe.whitelist()
def get_last_task_info(lead_name):
    # Récupérer la dernière tâche liée au lead
    last_task = frappe.db.get_value(
        "ToDo",
        filters={"reference_type": "Lead", "reference_name": lead_name},
        fieldname=["name", "allocated_to", "creation"],
        order_by="creation DESC",
        as_dict=True
    )

    if not last_task:
        return {
            "description": frappe._("No task found"),
            "date": frappe._("No task found"),
            "assigned_to": frappe._("No task found"),
        }

    # Récupérer le nom complet de l’utilisateur
    user_fullname = frappe.db.get_value("User", last_task.allocated_to, "full_name") or last_task.allocated_to
    description = frappe.db.get_value("ToDo", last_task.name, "description") or "Pas de description"

    return {
        "date": frappe.format(last_task.creation, {"fieldtype": "Date"}),
        "assigned_to": user_fullname,
        "description" : description
    }
