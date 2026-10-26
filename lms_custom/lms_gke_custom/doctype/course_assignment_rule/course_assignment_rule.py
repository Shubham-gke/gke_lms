import frappe
from frappe.model.document import Document

import requests
class CourseAssignmentRule(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from lms_custom.lms_gke_custom.doctype.course_based_on_rule.course_based_on_rule import CourseBasedOnRule

		course: DF.Table[CourseBasedOnRule]
		department: DF.Data
		designation: DF.Data
		is_active: DF.Check
	# end: auto-generated types

    # frappe.throw("lkjhgytdtfcghjbk")
	pass


