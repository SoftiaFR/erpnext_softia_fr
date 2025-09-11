import frappe
import re

from frappe.apps import _

def extend_column_if_needed(table, column):
    res = frappe.db.sql(f"SHOW COLUMNS FROM `tab{table}` LIKE '{column}'")
    current_type = res[0][1] if res else ""

    if "varchar(140)" in current_type.lower():
        frappe.db.sql_ddl(f"ALTER TABLE `tab{table}` MODIFY COLUMN `{column}` VARCHAR(255)")
        frappe.db.commit()
        print(_("{0}.{1} field extended to VARCHAR(255).").format(table, column))
    else:
        print(_("{0}.{1} already modified: {2}").format(table, column, current_type))


def extend_account_numbers():
    accounts = frappe.get_all("Account", fields=["name", "account_number", "account_name", "parent_account"])

    # Extend the size field
    extend_column_if_needed("Account", "name")
    extend_column_if_needed("Company", "default_inventory_account")
    extend_column_if_needed("Comment", "reference_name")

    for acc in accounts:
        acc_num = acc.get("account_number")
        acc_name = acc.get("account_name")
        old_name = acc["name"]

        # Case 1: Account with number
        if acc_num:
            new_acc_num = acc_num.ljust(8, "0")
            if acc_num != new_acc_num or not old_name.startswith(new_acc_num):
                old_name_parts = old_name.split(" - ", 1)
                rest_of_name = old_name_parts[1] if len(old_name_parts) > 1 else acc_name
                new_name = f"{new_acc_num} - {rest_of_name}"

                frappe.db.set_value("Account", old_name, "account_number", new_acc_num)
                # frappe.rename_doc("Account", old_name, new_name, force=True, merge=False)
                frappe.db.set_value("Account", old_name, "name", new_name)

        # Case 2: Account without a number, but the name begins with a digit
        else:
            match = re.match(r"^(\d+)\s*-\s*(.*)", old_name)
            if match:
                prefix_num = match.group(1).ljust(8, "0")
                rest_of_name = match.group(2) if match.group(2) else acc_name
                new_name = f"{prefix_num} - {rest_of_name}"

                if old_name != new_name:
                    # frappe.rename_doc("Account", old_name, new_name, force=True, merge=False)
                    frappe.db.set_value("Account", old_name, "name", new_name)

        # Case 3: Update the parent_account if necessary
        parent = acc.get("parent_account")
        if parent and re.match(r"^\d+", parent):
            parts = parent.split(" - ", 1)
            prefix_num = parts[0].ljust(8, "0")
            rest = parts[1] if len(parts) > 1 else ""
            new_parent = f"{prefix_num} - {rest}" if rest else prefix_num

            if parent != new_parent:
                frappe.db.set_value("Account", old_name, "parent_account", new_parent)

    frappe.db.commit()
    print(_("All accounts and parents have been modified."))



