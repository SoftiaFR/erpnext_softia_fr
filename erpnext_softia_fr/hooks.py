app_name = "erpnext_softia_fr"
app_title = "erpnext_softia_fr"
app_publisher = "Softia ingénierie"
app_description = "Integration de Siret"
app_email = ""
app_license = "mit"
app_logo_url = "/assets/erpnext_softia_fr/images/ERPNext_By_Softia_logo.png"


add_to_apps_screen = [
	{
		"name": "ERPNext_By_Softia",
		"logo": "/assets/erpnext_softia_fr/images/ERPNext_By_Softia_logo.png",
		"title": "ERPNext By Softia",
		"route": "/app/home",
		"has_permission": "erpnext.check_app_permission",
	}
]

doctype_js = {
    "Company": "public/js/siret_client.js",
    "Company": "public/js/company.js",
    "Opportunity": "public/js/opportunity.js",
    "Account": "public/js/account.js",
    "Sales Invoice": "public/js/sales_invoice.js",
    "Purchase Invoice": "public/js/purchase_invoice.js",
    "Sales Order": "public/js/sales_order.js",
    "Address": "public/js/address.js",
    "Notification": "public/js/notification.js",
    "Quality Procedure": "public/js/quality_procedure.js",
    "BOM": "public/js/bom.js",
    "Currency": "public/js/currency.js",
    "Journal Entry": "public/js/journal_entry.js",
    "Payment Entry": "public/js/payment_entry.js",
    "Holiday List": "public/js/holiday_list.js",
    "Production Plan": "public/js/production_plan.js",
    "Timesheet": "public/js/timesheet.js"
}
doctype_list_js = {
    "Dashboard": "public/js/dashboard_list.js",
    "Party Type": "public/js/party_type_list.js",
    "Lead": "public/js/lead_list.js",
}

after_install = "erpnext_softia_fr.setup.install.after_install"

#fixtures = [
#    {"dt": "Role", "filters": [["name", "in", ["Gestionnaire Global"]]]},
#    {"dt": "Custom DocPerm", "filters": [["role", "=", "Gestionnaire Global"]]},
#    {"dt": "Role Profile", "filters": [["name", "=", "Profil Gestionnaire Global"]]},
#]


# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "erpnext_softia_fr",
# 		"logo": "/assets/erpnext_softia_fr/logo.png",
# 		"title": "erpnext_softia_fr",
# 		"route": "/erpnext_softia_fr",
# 		"has_permission": "erpnext_softia_fr.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/erpnext_softia_fr/css/erpnext_softia_fr.css"
# app_include_js = "/assets/erpnext_softia_fr/js/erpnext_softia_fr.js"
app_include_css = "/assets/erpnext_softia_fr/css/custom_theme.css"
app_include_js = [
    "/assets/erpnext_softia_fr/js/custom_account_tree.js",
    "/assets/erpnext_softia_fr/js/trial_balance_for_party.js",
    "/assets/erpnext_softia_fr/js/custom_theme_handler.js",
    "/assets/erpnext_softia_fr/js/custom_logo.js",   
    "/assets/erpnext_softia_fr/js/brand.js",   
    "/assets/erpnext_softia_fr/js/task.js",   
    "/assets/erpnext_softia_fr/js/note.js",   
    "/assets/erpnext_softia_fr/js/asset_value_adjustment.js",   
    "/assets/erpnext_softia_fr/js/util.js"
]

# include js, css files in header of web template
# web_include_css = "/assets/erpnext_softia_fr/css/erpnext_softia_fr.css"
# web_include_js = "/assets/erpnext_softia_fr/js/erpnext_softia_fr.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "erpnext_softia_fr/public/scss/website"
website_context = {
	"favicon": "/assets/erpnext_softia_fr/images/ERPNext_By_Softia_logo.png",
	"splash_image": "/assets/erpnext_softia_fr/images/ERPNext_By_Softia_logo.png",
}

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}


# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "erpnext_softia_fr/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "erpnext_softia_fr.utils.jinja_methods",
# 	"filters": "erpnext_softia_fr.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "erpnext_softia_fr.install.before_install"
# after_install = "erpnext_softia_fr.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "erpnext_softia_fr.uninstall.before_uninstall"
# after_uninstall = "erpnext_softia_fr.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "erpnext_softia_fr.utils.before_app_install"
# after_app_install = "erpnext_softia_fr.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "erpnext_softia_fr.utils.before_app_uninstall"
# after_app_uninstall = "erpnext_softia_fr.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "erpnext_softia_fr.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"erpnext_softia_fr.tasks.all"
# 	],
# 	"daily": [
# 		"erpnext_softia_fr.tasks.daily"
# 	],
# 	"hourly": [
# 		"erpnext_softia_fr.tasks.hourly"
# 	],
# 	"weekly": [
# 		"erpnext_softia_fr.tasks.weekly"
# 	],
# 	"monthly": [
# 		"erpnext_softia_fr.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "erpnext_softia_fr.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "erpnext_softia_fr.event.get_events"
# }
override_whitelisted_methods = {
	"frappe.core.doctype.user.user.switch_theme": "erpnext_softia_fr.config.theme_switcher.switch_theme"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "erpnext_softia_fr.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["erpnext_softia_fr.utils.before_request"]
# after_request = ["erpnext_softia_fr.utils.after_request"]

# Job Events
# ----------
# before_job = ["erpnext_softia_fr.utils.before_job"]
# after_job = ["erpnext_softia_fr.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"erpnext_softia_fr.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

setup_wizard_complete = [
    "erpnext_softia_fr.setup.default_data.create_data",
    "erpnext_softia_fr.setup.translation_stock_entry_type.translation_stock_entry_type"
    ]
after_migrate = [
    "erpnext_softia_fr.api.account_custom_fields.execute",
    "erpnext_softia_fr.api.add_interim_safe.execute"
    ]

# TO DO after_migrate = ["erpnext_softia_fr.api.account_number_update.extend_account_numbers"]

