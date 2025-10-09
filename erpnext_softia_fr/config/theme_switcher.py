import frappe

@frappe.whitelist()
def switch_theme(theme):
	if theme in ["Dark", "Light", "Theme_softia", "Automatic"]:
		frappe.db.set_value("User", frappe.session.user, "desk_theme", theme)