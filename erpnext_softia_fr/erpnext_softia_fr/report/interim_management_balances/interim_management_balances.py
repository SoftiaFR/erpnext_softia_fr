import frappe
from frappe import _

def execute(filters=None):
    columns, data = [], []
    if filters is None:
        filters = {}

    # Colonnes du tableau (labels en anglais, translatables)
    columns = [
        {"label": _("SIG"), "fieldname": "sig", "fieldtype": "Data", "width": 200},
        {"label": _("Calculation"), "fieldname": "calcul", "fieldtype": "Data", "width": 250},
        {"label": _("Result"), "fieldname": "resultat", "fieldtype": "Currency", "width": 150, "options": "Company:company:default_currency"},
        {"label": _("% of Turnover"), "fieldname": "pourcent_ca", "fieldtype": "Float", "width": 100, "precision": 2},
    ]

    # Données SIG réelles
    data = get_sig_data(filters)

    return columns, data

def get_sig_data(filters):
    company = filters.get("company")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    
    if not all([company, from_date, to_date]):
        frappe.throw(_("Please select a company and a period."))  # Erreur en anglais, translatable
    
    # Mapping PCG français (classes de comptes pour SIG) – étendu pour CA total
    account_mapping = {
        'chiffre_affaires': ['70'],  # CA total (toutes ventes)
        'ventes_marchandises': ['707'],  # Ventes de marchandises (pour marge comm.)
        'achats_marchandises': ['607'],  # Coût d'achat marchandises vendues
        'production_vendue': ['701', '702', '703', '704', '705', '706', '708', '709'],  # Production vendue
        'production_stockee': ['71'],    # Production stockée
        'production_immobilisee': ['72'], # Production immobilisée
        'consommations_externes': ['601', '602', '603', '604', '605', '606', '608', '609', '61', '62'],  # Biens/services externes
        'charges_personnel': ['641', '642', '643', '644', '645', '646', '647', '648', '64'],  # Charges personnel
        'impots_taxes': ['635', '63'],   # Impôts et taxes
        'dotations_amort_provisions': ['681', '686', '687'],  # Amort. et provisions
        'produits_financiers': ['761', '762', '764', '766', '767', '768', '769'],  # Produits fin.
        'charges_financieres': ['661', '662', '664', '665', '666', '667', '668', '669'],  # Charges fin.
        'produits_exceptionnels': ['771', '774', '775', '776', '777', '778', '779'],  # Prod. exc.
        'charges_exceptionnelles': ['671', '674', '675', '676', '677', '678', '679'],  # Charges exc.
        'impots_benefices': ['695'],     # Impôt sur bénéfices
    }
    
    # Récupère les soldes réels
    ca_total = get_balance(company, from_date, to_date, account_mapping['chiffre_affaires'], debit=False)  # Crédit total CA
    ca_marge = get_balance(company, from_date, to_date, account_mapping['ventes_marchandises'], debit=False)  # Crédit pour marge
    cout_achat_march = get_balance(company, from_date, to_date, account_mapping['achats_marchandises'], debit=True)  # Débit
    prod_vendue = get_balance(company, from_date, to_date, account_mapping['production_vendue'], debit=False)
    prod_stockee = get_balance(company, from_date, to_date, account_mapping['production_stockee'], debit=False)
    prod_immob = get_balance(company, from_date, to_date, account_mapping['production_immobilisee'], debit=False)
    cons_externes = get_balance(company, from_date, to_date, account_mapping['consommations_externes'], debit=True)
    charges_pers = get_balance(company, from_date, to_date, account_mapping['charges_personnel'], debit=True)
    impots_taxes = get_balance(company, from_date, to_date, account_mapping['impots_taxes'], debit=True)
    dot_amort_prov = get_balance(company, from_date, to_date, account_mapping['dotations_amort_provisions'], debit=True)
    prod_fin = get_balance(company, from_date, to_date, account_mapping['produits_financiers'], debit=False)
    charges_fin = get_balance(company, from_date, to_date, account_mapping['charges_financieres'], debit=True)
    prod_exc = get_balance(company, from_date, to_date, account_mapping['produits_exceptionnels'], debit=False)
    charges_exc = get_balance(company, from_date, to_date, account_mapping['charges_exceptionnelles'], debit=True)
    impot_benef = get_balance(company, from_date, to_date, account_mapping['impots_benefices'], debit=True)
    
    # Calculs selon les formules EXACTES de ton doc
    marge_commerciale = ca_marge - cout_achat_march  # Marge commerciale = Ventes march. – Coût achat march. vendues
    production = prod_vendue + prod_stockee + prod_immob  # Production = Vendue + Stockée + Immobilisée
    va = (marge_commerciale + production) - cons_externes  # VA = (Marge + Production) – Cons. externes
    ebe = va - charges_pers - impots_taxes  # EBE = VA – Charges pers. – Impôts/taxes
    resultat_exploitation = ebe - dot_amort_prov  # Rés. expl. = EBE – Dot. amort./prov.
    rcai = resultat_exploitation + prod_fin - charges_fin  # RCAI = Rés. expl. + Prod. fin. – Charges fin.
    resultat_exceptionnel = prod_exc - charges_exc  # Rés. exc. = Prod. exc. – Charges exc.
    resultat_net = rcai + resultat_exceptionnel - impot_benef  # Rés. net = RCAI + Rés. exc. – Impôts bénéfices
    
    # Lignes du tableau avec formules textuelles réelles (suivant ton doc)
    data = [
        {
            "sig": _("Turnover"),  # English, translatable
            "calcul": f"{_('Total Sales')} ({ca_total})",  # English parts, translatable
            "resultat": ca_total,
            "pourcent_ca": 100.0
        },
        {
            "sig": _("Commercial Margin"),
            "calcul": f"{_('Sales of Merchandise')} ({ca_marge}) – {_('Cost of Purchased Goods Sold')} ({cout_achat_march})",
            "resultat": marge_commerciale,
            "pourcent_ca": (marge_commerciale / ca_total * 100) if ca_total else 0
        },
        {
            "sig": _("Production of the Exercise"),
            "calcul": f"{_('Sold Production')} ({prod_vendue}) + {_('Stocked Production')} ({prod_stockee}) + {_('Immobilized Production')} ({prod_immob})",
            "resultat": production,
            "pourcent_ca": (production / ca_total * 100) if ca_total else 0
        },
        {
            "sig": _("Value Added"),
            "calcul": f"({marge_commerciale} + {production}) – {_('External Consumptions')} ({cons_externes})",
            "resultat": va,
            "pourcent_ca": (va / ca_total * 100) if ca_total else 0
        },
        {
            "sig": _("EBE"),
            "calcul": f"{va} – {_('Personnel Charges')} ({charges_pers}) – {_('Taxes and Duties')} ({impots_taxes})",
            "resultat": ebe,
            "pourcent_ca": (ebe / ca_total * 100) if ca_total else 0
        },
        {
            "sig": _("Operating Result"),
            "calcul": f"{ebe} – {_('Depreciation and Provisions')} ({dot_amort_prov})",
            "resultat": resultat_exploitation,
            "pourcent_ca": (resultat_exploitation / ca_total * 100) if ca_total else 0
        },
        {
            "sig": _("RCAI"),
            "calcul": f"{resultat_exploitation} + {_('Financial Products')} ({prod_fin}) – {_('Financial Charges')} ({charges_fin})",
            "resultat": rcai,
            "pourcent_ca": (rcai / ca_total * 100) if ca_total else 0
        },
        {
            "sig": _("Exceptional Result"),
            "calcul": f"{_('Exceptional Products')} ({prod_exc}) – {_('Exceptional Charges')} ({charges_exc})",
            "resultat": resultat_exceptionnel,
            "pourcent_ca": (resultat_exceptionnel / ca_total * 100) if ca_total else 0
        },
        {
            "sig": _("Net Result"),
            "calcul": f"{rcai} + {resultat_exceptionnel} – {_('Taxes on Profits')} ({impot_benef})",
            "resultat": resultat_net,
            "pourcent_ca": (resultat_net / ca_total * 100) if ca_total else 0
        }
    ]
    return data

def get_balance(company, from_date, to_date, account_codes, debit=False):
    """
    Calcule le solde net (débit - crédit ou crédit - débit) pour une liste de codes de comptes.
    FIX: Échappement des % dans LIKE pour éviter l'erreur de format string.
    """
    if not account_codes:
        return 0.0
    
    # FIX: Double % pour échappement (%% devient % en SQL)
    conditions = [f"account LIKE '{code}%%'" for code in account_codes]
    where_accounts = " OR ".join(conditions)
    
    field_debit = "debit_in_account_currency"
    field_credit = "credit_in_account_currency"
    
    sql = f"""
        SELECT 
            COALESCE(SUM(CASE WHEN voucher_type != 'Journal Entry' OR (voucher_type = 'Journal Entry' AND is_advance = 'No') 
                              THEN {field_debit} ELSE 0 END), 0) AS total_debit,
            COALESCE(SUM(CASE WHEN voucher_type != 'Journal Entry' OR (voucher_type = 'Journal Entry' AND is_advance = 'No') 
                              THEN {field_credit} ELSE 0 END), 0) AS total_credit
        FROM `tabGL Entry`
        WHERE company = %s 
          AND posting_date BETWEEN %s AND %s 
          AND ({where_accounts})
          AND is_cancelled = 0
    """
    
    result = frappe.db.sql(sql, (company, from_date, to_date), as_dict=True)
    total_debit = result[0].total_debit if result else 0
    total_credit = result[0].total_credit if result else 0
    
    if debit:
        return total_debit - total_credit  # Solde débit net (positif pour charges)
    else:
        return total_credit - total_debit  # Solde crédit net (positif pour produits)