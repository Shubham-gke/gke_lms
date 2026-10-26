# Copyright (c) 2026, NA and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class PerformanceImprovementPlan(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from lms_custom.lms_gke_custom.doctype.courses_skills.courses_skills import CoursesSkills
		from lms_custom.lms_gke_custom.doctype.pip_courses.pip_courses import PipCourses

		amended_from: DF.Link | None
		employee_name: DF.Data | None
		pip_courses: DF.Table[PipCourses]
		pip_skills: DF.Table[CoursesSkills]
		reason: DF.Data | None
		user_id: DF.Link | None
	# end: auto-generated types

	_DOCTYPE_NAME = "Performance Improvement Plan"
