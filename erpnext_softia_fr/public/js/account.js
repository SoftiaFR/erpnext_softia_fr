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
        // frm.set_query("parent_account", function() {
        //     return {
        //         filters: [
        //             ["Account", "account_number", "like", "___"], // Corresponds to 3 digits
        //             ["Account", "is_group", "=", 1] 
        //         ]
        //     };
        // });

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
    if(frm.doc.account_number){
        let account_number = frm.doc.account_number.trim();
        if (!/^\d+$/.test(account_number)) {
            frappe.throw(__("The account number must contain only digits: {0}", [account_number]));
        }
        if (account_number.length > 8) {
            frappe.throw(__("The account number must contain exactly 8 digits : {0}", [account_number]));
        }
    }
    if (frm.doc.parent_account) {
        let parent_number = frm.doc.parent_account.split(" - ")[0]; 
        if(parent_number.length === 3){
            if(frm.doc.account_number){
                let account_number = frm.doc.account_number.trim();
                let parent_extended = parent_number.padEnd(8, "0");
                if (account_number.length <8) {
                    account_number = account_number.padEnd(8, "0");
                    frm.set_value("account_number", account_number);
                    frappe.throw(__("The account number must contain exactly 8 digits : {0}.", [account_number]));
                }
                if (account_number === parent_extended) {
                    frappe.throw(__("The account number cannot be the same as the parent account ({0}).", [parent_number]));
                }
                if (!account_number.startsWith(parent_number)) {
                    frappe.throw(
                        __("The account number must begin with the parent account ({0}).", [parent_number])
                    );
                }                
            }else{
                frappe.throw(__("The account number must contain exactly 8 digits : {0}", [account_number]));
            }
        }
    }
}

