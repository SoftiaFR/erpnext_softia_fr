# erpnext_softia_fr

**erpnext_softia_fr** est une application personnalisée (custom app) développée pour ERPNext. Elle permet l’intégration du numéro **SIRET** lors de la création d'une société (*Company*), conformément aux exigences des entreprises françaises, ainsi que d'autres customisations à venir.

## Fonctionnalités

- Ajout d’un champ **SIRET** dans le formulaire de création/modification de société
- Validation simple pour s'assurer que la valeur du champ SIRET est correct et existe réellement

## Installation

1. Cloner l’application depuis le dépôt Git :

```bash
bench get-app --branch develop erpnext_softia_fr https://git.soa.mg/softia/erpnext/Erpnext_Softia_Fr.git

```
2. Installer l'application sur le site ERPNext : 

```bash
bench --site nom_du_site install-app erpnext_softia_fr

```
3. Lancer l'application Frappe :

```bash
bench --site nom_du_site clear-cache
bench start

```
## Utilisation

1. Accéder à Société (ou Company) depuis l’interface ERPNext

2. Cliquer sur Nouveau/Nouvelle pour créer une nouvelle société

3. Remplir le champ SIRET visible dans le formulaire

4. Sauvegarder la société
>>>>>>> 469d97d (Renommage du custom app)
