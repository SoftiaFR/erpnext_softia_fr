import frappe
from frappe import _
import re

OVERRIDES = {
    "Repost Accounting Ledger Settings": (
        '<a href="/app/repost-accounting-ledger-settings">'
        'Repost Paramètres du livre comptable</a>'
    )
}

def translate_voucher_message(msg: str) -> str:
    try:
        if not re.search(r"repost|ledger|accounting", msg, re.IGNORECASE):
            return msg
        
        user_lang = frappe.local.lang if hasattr(frappe.local, "lang") else frappe.db.get_default("lang")
        if not user_lang or not user_lang.lower().startswith("fr"):
            return msg

        doctypes = frappe.get_all("DocType", pluck="name")

        for doctype in doctypes:
            translated = OVERRIDES.get(doctype, _(doctype))
            if not translated or translated == doctype:
                continue

            msg = msg.replace(doctype, translated)

            pattern = re.compile(r'(<a[^>]*>)' + re.escape(doctype) + r'(</a>)')
            msg = pattern.sub(r'\1{}\2'.format(translated), msg)

        parts = re.split(r"(is|are|n[’']?est|ne\s+sont)", msg, maxsplit=1, flags=re.IGNORECASE)
        if len(parts) > 1:
            doctype_part = parts[0].strip(" .:;!,'\"")
        else:
            doctype_part = msg.split(".")[0].strip(" .:;!,'\"")

        if re.search(r"\bet\b|\band\b", doctype_part, re.IGNORECASE):
            custom_msg = (
                f"{doctype_part} ne sont pas autorisées à être repostées. "
                "Modifiez "
                f"{OVERRIDES['Repost Accounting Ledger Settings']} "
                "pour permettre le transfert."
            )
        else:
            custom_msg = (
                f"{doctype_part} n’est pas autorisé à être reposté. "
                "Modifiez les "
                f"{OVERRIDES['Repost Accounting Ledger Settings']} "
                "pour permettre le transfert."
            )

        custom_msg = re.sub(r"\s{2,}", " ", custom_msg).strip()
        return custom_msg

    except Exception:
        return msg


def apply_permanent_throw_patch():
    if getattr(frappe, "_custom_throw_patched", False):
        return

    _original_throw = frappe.throw

    def custom_throw(msg=None, title=None, *args, **kwargs):
        if isinstance(msg, str):
            msg = translate_voucher_message(msg)
        return _original_throw(msg, title, *args, **kwargs)

    frappe.throw = custom_throw
    frappe._custom_throw_patched = True
