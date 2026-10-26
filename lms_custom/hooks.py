app_name = "lms_custom"
app_title = "lms_gke_custom"
app_publisher = "NA"
app_description = "NA"
app_email = "shubham_si@gkexport.com"
app_license = "mit"

# Send non-GET requests for this app's endpoints as native `application/json`
# bodies instead of form-encoded, per-key JSON-stringified values.
use_json_request_body = True

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "lms_custom",
# 		"logo": "/assets/lms_custom/logo.png",
# 		"title": "lms_gke_custom",
# 		"route": "/lms_custom",
# 		"has_permission": "lms_custom.api.permission.has_app_permission",
# 	}
# ]

# The dock, the rail down the left of the desk, is a document rather than a hook. Author it in
# Manage Dock on a developer-mode site and press Export to App, and it is written to
# `lms_custom/dock/lms_custom/lms_custom.json` for git to carry. An app that ships none has no
# rail: its sidebar gets a switcher in the header instead.
#
# A companion app, one that extends a host app rather than standing on its own, says so with
# `mount_on` on that same record, and its entries are appended to the host's rail. Mounting keeps
# the companion off the apps screen, so it takes precedence over any add_to_apps_screen above.

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/lms_custom/css/lms_custom.css"
# app_include_js = [
#     "/assets/lms_custom/js/similar_courses.js"
# ]

# include js, css files in header of web template
# web_include_css = "/assets/lms_custom/css/lms_custom.css"
# web_include_js = "/assets/lms_custom/js/similar_courses.js"
# update_website_context = "lms_custom.lms_gke_custom.api.course_assignment.inject_custom_js"
# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "lms_custom/public/scss/website"

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
# app_include_icons = "lms_custom/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Setup Wizard
# ------------

# open a fresh site's setup in this app's own UI instead of the desk wizard.
# must be a non-desk route (not under /desk or /app); to customize setup within
# desk, use setup_wizard_stages / setup_wizard_complete instead.
# setup_wizard_url = "/lms_custom/setup"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "lms_custom.utils.jinja_methods",
# 	"filters": "lms_custom.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "lms_custom.install.before_install"
# after_install = "lms_custom.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "lms_custom.uninstall.before_uninstall"
# after_uninstall = "lms_custom.uninstall.after_uninstall"

# Disable / Enable
# ----------------
# Called when this app is logically disabled or re-enabled on a site,
# without uninstalling it. Use this to hide/restore fields this app adds
# to other apps' doctypes.

# before_disable = "lms_custom.uninstall.before_disable"
# after_disable = "lms_custom.uninstall.after_disable"
# before_enable = "lms_custom.install.before_enable"
# after_enable = "lms_custom.install.after_enable"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "lms_custom.utils.before_app_install"
# after_app_install = "lms_custom.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "lms_custom.utils.before_app_uninstall"
# after_app_uninstall = "lms_custom.utils.after_app_uninstall"

# Build
# ------------------
# To hook into the build process

# after_build = "lms_custom.build.after_build"

# To hook into the build process of other apps
# The list of apps being built is passed as an argument

# after_app_build = "lms_custom.build.after_app_build"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "lms_custom.notifications.get_notification_config"

# Awesome Bar
# -----------
# Extra search results: list of dicts with label, description, route, index.
# route: ["List", "ToDo"], "/desk/docs/some/page", or "https://example.com"
# awesomebar_search = ["lms_custom.search.awesomebar_results"]

# Permissions
# -----------
# Permissions evaluated in scripted ways
# on_session_creation = "lms_custom.lms_gke_custom.api.course_assignment.on_session_creation"
# permission_query_conditions = {
# 	# "Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
#     "LMS Course": "lms_custom.lms_gke_custom.api.course_assignment.lms_course_permission_query"
# }

override_whitelisted_methods = {
    "lms.lms.utils.get_lesson": "lms_custom.lms_gke_custom.api.course_assignment.get_lesson_with_lock",
	"lms.lms.utils.get_courses":
		"lms_custom.lms_gke_custom.api.course_assignment.get_filtered_courses",
  
	# "lms.lms.utils.get_courses":"lms_custom.lms_gke_custom.api.course_assignment.validate_enrolled_course_skills",

	"lms.lms.api.get_my_courses":
		"lms_custom.lms_gke_custom.api.course_assignment.get_filtered_courses",
  
	"lms.lms.utils.get_course_details": "lms_custom.lms_gke_custom.api.course_assignment.get_course_details_with_skills",
}
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"LMS Enrollment": {
		"on_update": "lms_custom.lms_gke_custom.api.course_assignment.on_lms_enrollment_update",
  		# "before_insert": "lms_custom.lms_gke_custom.api.course_assignment.validate_enrollment_sequence"
    "LMS Course Progress": {
        "before_insert": "lms_custom.lms_gke_custom.api.course_assignment.validate_progress_insert"
    }
	}
}


# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"lms_custom.tasks.all"
# 	],
# 	"daily": [
# 		"lms_custom.tasks.daily"
# 	],
# 	"hourly": [
# 		"lms_custom.tasks.hourly"
# 	],
# 	"weekly": [
# 		"lms_custom.tasks.weekly"
# 	],
# 	"monthly": [
# 		"lms_custom.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "lms_custom.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "lms_custom.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#     "lms.lms.utils.get_lesson": "lms_custom.lms_gke_custom.api.course_assignment.get_lesson_with_lock"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "lms_custom.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["lms_custom.utils.before_request"]
# after_request = ["lms_custom.lms_gke_custom.inject_link.add_link"]

# Job Events
# ----------
# before_job = ["lms_custom.utils.before_job"]
# after_job = ["lms_custom.utils.after_job"]

# after_file_upload = ["lms_custom.utils.after_file_upload"]

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
# 	"lms_custom.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
export_python_type_annotations = True

# Require all whitelisted methods to have type annotations
require_type_annotated_api_methods = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

