import frappe
import requests
from requests.exceptions import RequestException

@frappe.whitelist()
def verifier_siret(siret):
    if not siret or len(siret) != 14 or not siret.isdigit():
        return {"status": "error", "message": "SIRET invalide (14 chiffres requis)"}

    api_url = f"https://data.siren-api.fr/v3/etablissements/{siret}"
    headers = {
        "X-Client-Secret": "o2alAmDMM9xZrQFis0zV7k6nY2lp6VOa",
        "Accept": "application/json"
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "status": "success",
            "data": {
                "siret": data["etablissement"]["siret"],
                "denomination": data["etablissement"]["unite_legale"]["denomination"],
                "adresse": f"{data['etablissement']['numero_voie']} {data['etablissement']['type_voie']} {data['etablissement']['libelle_voie']}",
                "code_postal": data["etablissement"]["code_postal"],
                "ville": data["etablissement"]["libelle_commune"],
                "activite_principale": data["etablissement"]["activite_principale"],
                "effectifs": data["etablissement"]["tranche_effectifs"]
            }
        }
    except RequestException as e:
        frappe.log_error("API Siren Error", f"Request failed: {str(e)}\nURL: {api_url}")
        return {"status": "error", "message": "Ce numéro SIRET est introuvable dans la base INSEE."}
