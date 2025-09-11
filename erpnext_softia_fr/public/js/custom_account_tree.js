(function () {
    // Validation only when leaving the field (blur)
    $(document).on('blur', 'input[data-fieldname="account_number"], textarea[data-fieldname="account_number"]', function (e) {
        const $input = $(this);
        let val = ($input.val() || '').trim();

        $input.removeClass('invalid-account-number');
        $input.closest('.form-group, .control-input-wrapper').find('.account-number-error').remove();

        if (!val) return;

        if (!/^\d+$/.test(val)) {
            frappe.throw(__("The account number must contain only numbers."));
        }

        if (val.length > 8) {
            frappe.throw(__("The account number must not exceed 8 digits."));
        }

        if (val.length < 8) {
            val = val.padEnd(8, "0");
            $input.val(val);
            frappe.throw(__("The account number must be exactly 8 digits long. It has been auto-padded to: {0}.", [val]));
        }
    });

    $(document).on('click', '.modal .modal-footer .btn-primary, .frappe-dialog .modal-footer .btn-primary, .frappe-dialog .primary-action', function (e) {
        const $btn = $(this);
        const $dialog = $btn.closest('.modal, .frappe-dialog');
        if (!$dialog.length) return;

        const $input = $dialog.find('input[data-fieldname="account_number"], textarea[data-fieldname="account_number"]');
        if (!$input.length) return;

        const val = ($input.val() || '').trim();

        if (val && !/^\d+$/.test(val)) {
            e.preventDefault(); e.stopImmediatePropagation();
            frappe.msgprint(__("The account number must contain only numbers."));
            $input.focus();
            return false;
        }

        if (val && val.length > 8) {
            e.preventDefault(); e.stopImmediatePropagation();
            frappe.msgprint(__("The account number must not exceed 8 digits."));
            $input.focus();
            return false;
        }
        if (val.length < 8) {
            val = val.padEnd(8, "0");
            $input.val(val);
            frappe.throw(__("The account number must be exactly 8 digits long. It has been auto-padded to: {0}.", [val]));
            $input.focus();
            return false;            
        }        
    });    
})();
