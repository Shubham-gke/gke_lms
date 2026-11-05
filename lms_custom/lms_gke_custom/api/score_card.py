# ------------------------------------------------------------------
# Save as:
#   lms_custom/lms_gke_custom/api/score_card.py
#
# (If that file already exists, just add the function below to it.)
# ------------------------------------------------------------------

import frappe


@frappe.whitelist(allow_guest=True)
def get_score_card_users():
    """
    Returns the employees an admin can pick in the Score Card page.

    Result: [{"name": "user@example.com", "full_name": "Employee Name"}, ...]
    Only System Manager / Administrator can call this.
    """
    roles = frappe.get_roles()
    # frappe.throw(f"{roles}")
    if "System Manager" not in roles and "Administrator" not in roles:
        frappe.throw("Not permitted", frappe.PermissionError)

    # Site has the Employee doctype (HRMS): list active employees that have a user
    if frappe.db.exists("DocType", "Employee"):
        return frappe.get_all(
            "Employee",
            filters={"status": "Active", "user_id": ["is", "set"]},
            fields=["user_id as name", "employee_name as full_name"],
            order_by="employee_name asc",
            limit_page_length=0,
        )

    # LMS-only site (no Employee doctype): list enabled users instead
    return frappe.get_all(
        "User",
        filters={
            "enabled": 1,
            "name": ["not in", ["Administrator", "Guest"]],
        },
        fields=["name", "full_name"],
        order_by="full_name asc",
        limit_page_length=0,
    )