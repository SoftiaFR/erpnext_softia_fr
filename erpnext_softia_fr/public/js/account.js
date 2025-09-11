frappe.ui.form.on("Account", {
    validate: function(frm) {
        account_number_validation(frm);
    },
    refresh: function(frm) {
        frm.set_query("super_parent", function() {
            return {
                filters: [
                    ["Account", "account_number", "in", ["1", "2", "3", "4", "5", "6", "7"]]
                ]
            };
        });
    },
    account_number: function(frm) {
        account_number_validation(frm);
    },    
    parent_account: function(frm) {
        if (frm.doc.parent_account) {
            let parent_number = frm.doc.parent_account.split(" - ")[0];
            let first_digit = parent_number.charAt(0);

            frappe.db.get_value("Account", { "account_number": first_digit }, "name")
                .then(r => {
                    if (r && r.message && r.message.name) {
                        frm.set_value("super_parent", r.message.name);
                    }
                });
        }
    }
});
function account_number_validation(frm) {
    if (frm.doc.account_number) {
        let account_number = frm.doc.account_number.trim();

        if (!/^\d+$/.test(account_number)) {
            frappe.throw(__("The account number must contain only digits: {0}", [account_number]));
        }

        if (account_number.length < 8) {
            account_number = account_number.padEnd(8, "0");
            frm.set_value("account_number", account_number);
            frappe.throw(__("The account number must be exactly 8 digits long. It has been auto-padded to: {0}.", [account_number]));
        }
                  
        if (account_number.length > 8) {
            frappe.throw(__("The account number must contain exactly 8 digits: {0}", [account_number]));
        }

    }

    if (frm.doc.parent_account) {
        let parent_number = frm.doc.parent_account.split(" - ")[0].trim();

        if (frm.doc.account_number) {
            let account_number = frm.doc.account_number.trim();


            if (account_number === parent_number) {
                frappe.throw(__("The account number cannot be the same as the parent account ({0}).", [parent_number]));
            }

            if (!account_number.startsWith(parent_number.substring(0, 1))) {
                frappe.throw(
                    __("The account number must begin with the parent account prefix ({0}).", [parent_number])
                );
            }
        }
    }
}
