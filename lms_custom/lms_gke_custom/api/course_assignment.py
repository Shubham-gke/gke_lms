# import frappe
# import requests
# # frappe.throw("kl?ljhghfgdxgfgvhbjnk;")
# @frappe.whitelist(allow_guest=True)
# def get_employee_dept_designation(user: str | None = None):
# 	"""HRMS API se saare employees lao, current user ka record dhoondo"""
# 	api_url = "http://ec2-13-234-27-130.ap-south-1.compute.amazonaws.com:8001/api/method/lms_des_dept"

# 	try:
# 		response = requests.get(api_url, timeout=10)
# 		response.raise_for_status()
# 		data = response.json().get("message", [])
# 		# frappe.msgprint(f"{data}")
# 	except Exception:
# 		frappe.log_error(frappe.get_traceback(), "Employee API Call Failed")
# 		return None, None

# 	for emp in data:
# 		if emp.get("user_id") == user:
# 			return emp.get("department"), emp.get("designation")

# 	return None, None


# # def get_matched_courses(department, designation):
# #     """Course Assignment Rule se match hone wale courses nikaalo"""

# #     if not department or not designation:
# #         return []

# #     rules = frappe.get_all(
# #         "Course Assignment Rule",
# #         filters={
# #             "department": department,
# #             "designation": designation,
# #             "is_active": 1
# #         },
# #         fields=["name"]
# #     )

# #     allowed_courses = []

# #     for rule in rules:
# #         courses = frappe.get_all(
# #             "Course Based On Rule",
# #             filters={
# #                 "parent": rule.name,
# #                 "parenttype": "Course Assignment Rule"
# #             },
# #             fields=["course"]
# #         )

# #         allowed_courses.extend(
# #             [row.course for row in courses if row.course]
# #         )
		
# #     # frappe.throw(allowed_courses)
# #     return allowed_courses

# def get_matched_courses(department, designation):
# 	"""Course Assignment Rule se match hone wale courses nikaalo, order (idx) ke saath"""
# 	if not department or not designation:
# 		return []

# 	rule_names = frappe.get_all(
# 		"Course Assignment Rule",
# 		filters={
# 			"department": department,
# 			"designation": designation,
# 			"is_active": 1
# 		},
# 		pluck="name"
# 	)

# 	if not rule_names:
# 		return []

# 	course_rows = frappe.get_all(
# 		"Course Based On Rule",   # apna child doctype naam confirm kar lena
# 		filters={"parent": ["in", rule_names]},
# 		fields=["course", "idx", "parent"],
# 		order_by="parent, idx"
# 	)

# 	# duplicate course hata do, order waise hi rakho (pehli baar jahan aaya wahi rahega)
# 	seen = set()
# 	ordered_courses = []
# 	for row in course_rows:
# 		if row.course not in seen:
# 			seen.add(row.course)
# 			ordered_courses.append(row.course)

# 	return ordered_courses



# def auto_enroll_courses(user):
# 	# frappe.throw("herrerer",user)
# 	"""Sirf agla incomplete course enroll karo — order ke hisaab se"""
# 	if user in ("Administrator", "Guest"):
# 		return

# 	department, designation = get_employee_dept_designation(user)
# 	if not department or not designation:
# 		return

# 	ordered_courses = get_matched_courses(department, designation)
# 	if not ordered_courses:
# 		return

# 	for course in ordered_courses:
# 		enrollment = frappe.db.get_value(
# 			"LMS Enrollment",
# 			{"member": user, "course": course},
# 			["name", "progress"],
# 			as_dict=True
# 		)

# 		if enrollment:
# 			if (enrollment.progress or 0) >= 100:
# 				frappe.throw("herrerer")
# 				# ye complete ho chuka, agle course ki taraf badho
# 				continue
# 			else:
# 				# ye abhi in-progress hai, yahin ruk jao
# 				return
# 		else:
# 			# ye course enroll hi nahi hua, ab isi ko enroll karo
# 			try:
# 				new_enrollment = frappe.new_doc("LMS Enrollment")
# 				new_enrollment.member = user
# 				new_enrollment.course = course
# 				new_enrollment.insert(ignore_permissions=True)
# 				frappe.db.commit()
# 			except Exception:
# 				frappe.log_error(frappe.get_traceback(), f"Auto Enroll Failed: {user} - {course}")
# 			return


# def on_lms_enrollment_update(doc, method):
# 	"""Jab enrollment progress update ho, turant agla course check karo"""
# 	if (doc.progress or 0) >= 100:
# 		auto_enroll_courses(doc.member)
  


# def on_session_creation(login_manager):
# 	"""Login hote hi ye chalega"""
# 	auto_enroll_courses(frappe.session.user)


# @frappe.whitelist(allow_guest=True)
# def get_filtered_courses(filters: dict = None, start: int = 0, limit_page_length: int | str = None, **kwargs):
# 	"""
# 	LMS ke 'Courses' page (frontend) ki API ko override karke
# 	sirf matched courses return karo.
# 	"""
# 	from lms.lms.utils import get_courses as original_get_courses
 

# 	user = frappe.session.user

# 	# frappe.throw(";lklhgjfdxgfchgjbjn")
 
# 	if user in ("Administrator", "Guest") or "System Manager" in frappe.get_roles(user):
# 		return original_get_courses(filters=filters, start=start, limit_page_length=limit_page_length)

# 	department, designation = get_employee_dept_designation(user)
# 	allowed_courses = get_matched_courses(department, designation)
# 	# frappe.throw(str(allowed_courses))

# 	all_courses = original_get_courses(filters=filters, start=start, limit_page_length=limit_page_length)

# 	# get_courses ek list return karta hai (dict nahi), har course ek dict hai jisme 'name' field hai
# 	return [c for c in all_courses if c.get("name") in allowed_courses]



# import json


# @frappe.whitelist(allow_guest=True)
# def get_employee_lms_data(user: str | None = None):
# 	"""
# 	User ke saare LMS Enrollment nikaalo, har course ke quiz(zes) dhoondo,
# 	aur us user ki quiz submission se score nikaalo.
# 	"""
# 	user = user or frappe.session.user

# 	enrollments = frappe.get_all(
# 		"LMS Enrollment",
# 		filters={"member": user},
# 		fields=["name", "course", "progress", "creation"],
# 	)

# 	result = []

# 	for enrollment in enrollments:
# 		course = enrollment.course

# 		course_title = frappe.db.get_value(
# 			"LMS Course",
# 			course,
# 			"title"
# 		)

# 		quiz_ids = []

# 		lessons = frappe.get_all(
# 			"Course Lesson",
# 			filters={"course": course},
# 			fields=["name", "content"]
# 		)

# 		for lesson in lessons:
# 			if not lesson.content:
# 				continue

# 			try:
# 				content = json.loads(lesson.content)

# 				for block in content.get("blocks", []):
# 					if block.get("type") == "quiz":
# 						quiz_id = block.get("data", {}).get("quiz")

# 						if quiz_id and quiz_id not in quiz_ids:
# 							quiz_ids.append(quiz_id)

# 			except Exception:
# 				continue

# 		quiz_results = []

# 		for quiz_id in quiz_ids:
# 			quiz = frappe.db.get_value(
# 				"LMS Quiz",
# 				quiz_id,
# 				["name", "title"],
# 				as_dict=True
# 			)

# 			if not quiz:
# 				continue

# 			submission = frappe.db.get_value(
# 				"LMS Quiz Submission",
# 				{
# 					"member": user,
# 					"quiz": quiz.name
# 				},
# 				["name", "score", "percentage", "creation"],
# 				as_dict=True,
# 			)

# 			quiz_results.append(
# 				{
# 					"quiz": quiz.name,
# 					"quiz_title": quiz.title,
# 					"attempted": bool(submission),
# 					"score": submission.score if submission else None,
# 					"percentage": (
# 						submission.percentage
# 						if submission
# 						else None
# 					),
# 					"submitted_on": (
# 						str(submission.creation)
# 						if submission
# 						else None
# 					),
# 				}
# 			)

# 		attempted_scores = [
# 			q["percentage"]
# 			for q in quiz_results
# 			if q["percentage"] is not None
# 		]

# 		avg_quiz_pct = (
# 			round(
# 				sum(attempted_scores) / len(attempted_scores),
# 				1
# 			)
# 			if attempted_scores
# 			else None
# 		)

# 		result.append(
# 			{
# 				"course": course,
# 				"course_title": course_title,
# 				"progress": enrollment.progress or 0,
# 				"enrolled_on": str(enrollment.creation),
# 				"quizzes": quiz_results,
# 				"avg_quiz_percentage": avg_quiz_pct,
# 			}
# 		)

# 	return {
# 		"user": user,
# 		"courses": result,
# 	}




import frappe
import requests
import json


HRMS_API_URL = "http://ec2-13-234-27-130.ap-south-1.compute.amazonaws.com:8001/api/method/lms_des_dept"


@frappe.whitelist(allow_guest=True)
def get_employee_dept_designation(user: str | None = None) -> tuple:
	"""Fetch department, designation, skills and goals from the HRMS API."""
	# frappe.throw("lkjhugtfdrtfyguh")
	user = user or frappe.session.user

	if not user or user == "Guest":
		return None, None, [], []

	api_url = frappe.conf.get("hrms_api_url") or HRMS_API_URL

	headers = {}
	api_key = frappe.conf.get("hrms_api_key")
	api_secret = frappe.conf.get("hrms_api_secret")
	if api_key and api_secret:
		headers["Authorization"] = f"token {api_key}:{api_secret}"

	try:
		# frappe.throw("kjhgjk")
		response = requests.get(
			api_url,
			params={"user_id": user},
			# headers=headers,
			timeout=10,
		)
		response.raise_for_status()
		data = response.json().get("message") or {}
		# frappe.throw(f"{data}")

	except Exception as e:
		# frappe.throw(str(e))
		frappe.log_error(
			title="Employee API Call Failed",
			message=frappe.get_traceback(),
		)
		return None, None, [], []

	if isinstance(data, list):
		data = next((emp for emp in data if emp.get("user_id") == user), {})

	return (
		data.get("department"),
		data.get("designation"),
		data.get("skills") or [],
		data.get("goals") or [],
	)
 
 
def get_matched_courses(department, designation):
	"""Course Assignment Rule ke according ordered courses return karo."""

	if not department or not designation:
		return []

	rule_names = frappe.get_all(
		"Course Assignment Rule",
		filters={
			"department": department,
			"designation": designation,
			"is_active": 1
		},
		pluck="name"
	)
 
	# frappe.throw(f"{rule_names}")

	if not rule_names:
		return []

	course_rows = frappe.get_all(
		"Course Based On Rule",
		filters={
			"parent": ["in", rule_names]
		},
		fields=[
			"course",
			"idx",
			"parent"
		],
		order_by="parent, idx"
	)
 
	# frappe.throw(f"{course_rows}")

	seen = set()
	ordered_courses = []

	for row in course_rows:
		if row.course and row.course not in seen:
			seen.add(row.course)
			ordered_courses.append(row.course)
	# frappe.throw(f"{ordered_courses}")	
	return ordered_courses


def get_user_ordered_courses(user):
	"""User ke department/designation ke according courses."""

	department, designation = get_employee_dept_designation(user)

	if not department or not designation:
		return []

	return get_matched_courses(
		department,
		designation
	)


def get_course_progress(user, course):
	"""User ke course ka progress."""

	progress = frappe.db.get_value(
		"LMS Enrollment",
		{
			"member": user,
			"course": course
		},
		"progress"
	)

	return progress or 0


def get_current_course(user):
	"""
	First incomplete/un-enrolled course return karega.
	"""

	ordered_courses = get_user_ordered_courses(user)

	if not ordered_courses:
		return None

	for course in ordered_courses:

		enrollment = frappe.db.get_value(
			"LMS Enrollment",
			{
				"member": user,
				"course": course
			},
			[
				"name",
				"progress"
			],
			as_dict=True
		)

		if not enrollment:
			return course

		if (enrollment.progress or 0) < 100:
			return course

	return None


def check_course_access(user, course):
	"""
	Course enroll/open karne se pehle check karega.

	First course:
		Allowed

	Second course:
		First course 100% hona chahiye

	Third course:
		Second course 100% hona chahiye
	"""

	if user in ("Administrator", "Guest"):
		return True

	if "System Manager" in frappe.get_roles(user):
		return True

	ordered_courses = get_user_ordered_courses(user)

	if not ordered_courses:
		frappe.throw(
			"No courses assigned to you."
		)

	if course not in ordered_courses:
		frappe.throw(
			"This course is not assigned to you."
		)

	current_index = ordered_courses.index(course)

	# First course
	if current_index == 0:
		return True

	previous_course = ordered_courses[current_index - 1]

	previous_progress = frappe.db.get_value(
		"LMS Enrollment",
		{
			"member": user,
			"course": previous_course
		},
		"progress"
	)

	previous_progress = previous_progress or 0

	if previous_progress < 100:
		frappe.throw(
			f"Please complete '{previous_course}' before starting '{course}'."
		)

	return True


def get_course_lock_status(user, course):
	"""
	Frontend ke liye course ka locked/unlocked status.
	"""

	if user in ("Administrator", "Guest"):
		return False

	if "System Manager" in frappe.get_roles(user):
		return False

	ordered_courses = get_user_ordered_courses(user)

	if not ordered_courses:
		return True

	if course not in ordered_courses:
		return True

	current_index = ordered_courses.index(course)

	# First course always unlocked
	if current_index == 0:
		return False

	previous_course = ordered_courses[current_index - 1]

	previous_progress = frappe.db.get_value(
		"LMS Enrollment",
		{
			"member": user,
			"course": previous_course
		},
		"progress"
	)

	previous_progress = previous_progress or 0

	return previous_progress < 100


def auto_enroll_courses(user):
	"""
	Sirf next eligible course enroll karega — ek call mein max 1 course.

	Example:

	Course 1 = not enrolled
	-> Course 1 enroll, stop

	Course 1 = 50%
	-> stop (abhi incomplete hai)

	Course 1 = 100%
	-> Course 2 enroll, stop

	Course 2 = 50%
	-> stop

	Course 2 = 100%
	-> Course 3 enroll, stop
	"""

	if user in ("Administrator", "Guest"):
		return

	ordered_courses = get_user_ordered_courses(user)

	if not ordered_courses:
		return

	for course in ordered_courses:

		enrollment = frappe.db.get_value(
			"LMS Enrollment",
			{
				"member": user,
				"course": course
			},
			[
				"name",
				"progress"
			],
			as_dict=True
		)

		if enrollment:

			progress = enrollment.progress or 0

			# Current course complete hai
			# next course par jao
			if progress >= 100:
				continue

			# Current course incomplete hai
			# yahin ruk jao — aur kuch enroll mat karo
			return

		# Course enrolled nahi hai — isi ko enroll karo
		try:

			new_enrollment = frappe.new_doc(
				"LMS Enrollment"
			)

			new_enrollment.member = user
			new_enrollment.course = course

			new_enrollment.insert(
				ignore_permissions=True
			)

			frappe.db.commit()

		except Exception:

			frappe.log_error(
				frappe.get_traceback(),
				f"Auto Enroll Failed: {user} - {course}"
			)

		# Important:
		# ek execution me sirf ek course enroll hoga
		return


def on_lms_enrollment_update(doc, method):
	"""
	Current course 100% complete hone par
	next course automatically enroll karega.
	"""

	if (doc.progress or 0) >= 100:
		auto_enroll_courses(
			doc.member
		)


def on_session_creation(login_manager):
	"""
	Login ke time eligible course enroll karo.
	"""

	auto_enroll_courses(
		frappe.session.user
	)

# SIMILAR_COURSE_ID = "similar-courses"
@frappe.whitelist(allow_guest=True)
def get_filtered_courses(
	filters: dict = None,
	start: int = 0,
	limit_page_length: int | str = None,
	**kwargs
):
	"""
	Sirf assigned courses dikhayega (allowed_courses se match hone wale).
	"""

	from lms.lms.utils import get_courses as original_get_courses

	user = frappe.session.user

	if user in ("Administrator", "Guest"):
		return original_get_courses(
			filters=filters,
			start=start,
			limit_page_length=limit_page_length
		)

	if "System Manager" in frappe.get_roles(user):
		return original_get_courses(
			filters=filters,
			start=start,
			limit_page_length=limit_page_length
		)

	department, designation, skills, goals = get_employee_dept_designation(
		user
	)

	allowed_courses = get_matched_courses(
		department,
		designation
	)
 
	# frappe.throw(f"{allowed_courses}")

	if not allowed_courses:
		return []

	all_courses = original_get_courses(
		filters=filters,
		start=start,
		limit_page_length=limit_page_length
	)
	# frappe.throw(f"{all_courses}")
	# Assigned courses
	courses = [
		course
		for course in all_courses
		if course.get("name") in allowed_courses
	]
 
	# ye line tab use hogi jab lms me koi courses auto assing hoga validate_enrolled_course_skills ye wali api se for their low score in skills kyuki ye direct insert hota
	# lms enrollemnt me aur add nhi ho pata get_courses ke apis me kyuki vo courses ass rule se aaata h 

	# courses me jo names already hain
	existing_names = {c.get("name") for c in courses}

	# user ke LMS Enrollment ke saare course names
	enrolled_courses = frappe.get_all(
		"LMS Enrollment",
		filters={"member": user},
		pluck="course"
	)

	# wo course names jo enrollment me hain lekin courses me nahi hain
	missing_names = [c for c in set(enrolled_courses) if c not in existing_names]

	# unke full course objects (all_courses me se)
	get_all_lms_courses_not_in_courses = [
		course
		for course in all_courses
		if course.get("name") in missing_names
	]

	# courses me add kar do
	courses.extend(get_all_lms_courses_not_in_courses)


	return courses


@frappe.whitelist()
def check_course_access_api(course):
	"""
	Frontend se course access check karne ke liye API.
	"""

	user = frappe.session.user

	check_course_access(
		user,
		course
	)

	return {
		"allowed": True,
		"course": course
	}


@frappe.whitelist()
def get_course_lock_status_api(course):
	"""
	Frontend ko locked/unlocked status deta hai.
	"""

	user = frappe.session.user

	locked = get_course_lock_status(
		user,
		course
	)

	return {
		"course": course,
		"locked": locked,
		"allowed": not locked
	}


@frappe.whitelist()
def get_my_course_status():
	"""
	Assigned courses ke saath progress aur lock status return karega.
	Frontend ke liye useful hai.
	"""

	user = frappe.session.user

	if user in ("Administrator", "Guest"):
		return []

	ordered_courses = get_user_ordered_courses(
		user
	)

	result = []

	for index, course in enumerate(ordered_courses):

		progress = get_course_progress(
			user,
			course
		)

		enrollment = frappe.db.get_value(
			"LMS Enrollment",
			{
				"member": user,
				"course": course
			},
			"name"
		)

		locked = get_course_lock_status(
			user,
			course
		)

		course_title = frappe.db.get_value(
			"LMS Course",
			course,
			"title"
		)

		result.append(
			{
				"course": course,
				"course_title": course_title,
				"order": index + 1,
				"progress": progress,
				"enrolled": bool(enrollment),
				"locked": locked,
				"allowed": not locked
			}
		)

	return result


@frappe.whitelist(allow_guest=True)
def get_employee_lms_data(user: str | None = None):
	"""
	User ke LMS Enrollment + Quiz data.
	"""
 
	department, designation, skills, goals = get_employee_dept_designation(
		user
	)
 
	# frappe.throw(f"{department, designation, skills, goals}")

	user = user or frappe.session.user

	enrollments = frappe.get_all(
		"LMS Enrollment",
		filters={
			"member": user
		},
		fields=[
			"name",
			"course",
			"progress",
			"creation"
		],
		order_by="creation asc"
	)

	result = []

	for enrollment in enrollments:

		course = enrollment.course

		course_title = frappe.db.get_value(
			"LMS Course",
			course,
			"title"
		)

		quiz_ids = []

		lessons = frappe.get_all(
			"Course Lesson",
			filters={
				"course": course
			},
			fields=[
				"name",
				"content"
			]
		)

		for lesson in lessons:

			if not lesson.content:
				continue

			try:

				content = json.loads(
					lesson.content
				)

				for block in content.get(
					"blocks",
					[]
				):

					if block.get("type") == "quiz":

						quiz_id = block.get(
							"data",
							{}
						).get("quiz")

						if (
							quiz_id
							and quiz_id not in quiz_ids
						):
							quiz_ids.append(
								quiz_id
							)

			except Exception:
				continue

		quiz_results = []

		for quiz_id in quiz_ids:

			quiz = frappe.db.get_value(
				"LMS Quiz",
				quiz_id,
				[
					"name",
					"title"
				],
				as_dict=True
			)

			if not quiz:
				continue

			submission = frappe.db.get_value(
				"LMS Quiz Submission",
				{
					"member": user,
					"quiz": quiz.name
				},
				[
					"name",
					"score",
					"percentage",
					"creation"
				],
				as_dict=True
			)

			quiz_results.append(
				{
					"quiz": quiz.name,
					"quiz_title": quiz.title,
					"attempted": bool(
						submission
					),
					"score": (
						submission.score
						if submission
						else None
					),
					"percentage": (
						submission.percentage
						if submission
						else None
					),
					"submitted_on": (
						str(
							submission.creation
						)
						if submission
						else None
					)
				}
			)

		attempted_scores = [
			q["percentage"]
			for q in quiz_results
			if q["percentage"] is not None
		]

		avg_quiz_pct = (
			round(
				sum(attempted_scores)
				/ len(attempted_scores),
				1
			)
			if attempted_scores
			else None
		)

		result.append(
			{
				"course": course,
				"course_title": course_title,
				"progress": enrollment.progress or 0,
				"enrolled_on": str(
					enrollment.creation
				),
				"quizzes": quiz_results,
				"avg_quiz_percentage": avg_quiz_pct
			}
		)

	return {
		"user": user,
		"department": department,
		"skills":skills,
		"goals":goals,
		"designation": designation,
		"courses": result
	}


@frappe.whitelist()
def enroll_in_course(course):
	"""
	User manually kisi course ko enroll karne ki try kare
	to pehle sequence validation hogi — sirf sahi "next" course
	hi enroll ho sakta hai, order todkar nahi.
	"""

	user = frappe.session.user

	if user in ("Administrator", "Guest"):
		frappe.throw("Invalid user.")

	if "System Manager" not in frappe.get_roles(user):
		# Ye khud throw kar dega agar sequence galat ho
		check_course_access(user, course)

	existing = frappe.db.exists(
		"LMS Enrollment",
		{
			"member": user,
			"course": course
		}
	)

	if existing:
		return {
			"success": True,
			"message": "Already enrolled.",
			"enrollment": existing
		}

	try:

		enrollment = frappe.new_doc(
			"LMS Enrollment"
		)

		enrollment.member = user
		enrollment.course = course

		enrollment.insert(
			ignore_permissions=True
		)

		frappe.db.commit()

		return {
			"success": True,
			"message": "Course enrolled successfully.",
			"enrollment": enrollment.name
		}

	except Exception:

		frappe.log_error(
			frappe.get_traceback(),
			f"Manual Course Enrollment Failed: {user} - {course}"
		)

		frappe.throw(
			"Unable to enroll in course."
		)
  
import json
import frappe
from lms.lms.utils import get_lesson as original_get_lesson, get_lessons

BYPASS_ROLES = {"Course Creator", "Moderator", "System Manager"}


def get_lesson_names(course: str):
    """Course ke saare lessons ke names, chapter order mein."""
    lessons = get_lessons(course)
    return [l.get("name") if isinstance(l, dict) else l.name for l in lessons]


def get_lesson_name(course: str, chapter, lesson):
    """URL ke chapter/lesson index se lesson ka actual name nikalta hai."""
    chapter_name = frappe.db.get_value(
        "Chapter Reference", {"parent": course, "idx": int(chapter)}, "chapter"
    )
    if not chapter_name:
        return None
    return frappe.db.get_value(
        "Lesson Reference", {"parent": chapter_name, "idx": int(lesson)}, "lesson"
    )


def validate_course_progress(course, lesson_name, user=None):
    """
    None -> allowed
    str  -> locked, string = pehla incomplete lesson jo complete karna hai
    """
    user = user or frappe.session.user

    if user in ("Administrator", "Guest"):
        return None
    if BYPASS_ROLES & set(frappe.get_roles(user)):
        return None

    names = get_lesson_names(course)
    if not names or lesson_name not in names:
        return None

    pos = names.index(lesson_name)
    if pos == 0:
        return None

    previous = names[:pos]
    completed = set(
        frappe.get_all(
            "LMS Course Progress",
            filters={"member": user, "lesson": ["in", previous], "status": "Complete"},
            pluck="lesson",
        )
    )

    for n in previous:
        if n not in completed:
            return n  # pehla incomplete lesson

    return None

def locked_lesson_response(data: dict, message: str):
    """Asli content hata kar sirf message wala lesson return karta hai."""
    data["content"] = json.dumps({
        "time": 0,
        "blocks": [
            {"id": "locked1", "type": "header",
             "data": {"text": "🔒 Lesson Locked", "level": 2}},
            {"id": "locked2", "type": "paragraph",
             "data": {"text": message}},
        ],
        "version": "2.29.0",
    })
    data["body"] = None
    data["youtube"] = None
    data["quiz_id"] = None
    data["question"] = None
    data["file_type"] = ""
    data["instructor_notes"] = None
    data["videos"] = []
    data["progress"] = None
    data["next"] = None
    data["is_locked"] = 1
    return data


@frappe.whitelist(allow_guest=True)
def get_lesson_with_lock(course: str, chapter: int | str, lesson: int | str):
    user = frappe.session.user
    data = original_get_lesson(course, chapter, lesson)

    if user == "Guest":
        return data

    lesson_name = get_lesson_name(course, chapter, lesson)
    if not lesson_name:
        return data

    prev_lesson = validate_course_progress(course, lesson_name, user)

    if prev_lesson:  # locked
        prev_title = frappe.db.get_value("Course Lesson", prev_lesson, "title") or prev_lesson

        return locked_lesson_response(
            data,
            f"First complete <b>{prev_title}</b> lesson Then Proceed Further.",
        )

    return data


def validate_progress_insert(doc, method=None):
    """Complete mark karte waqt: locked lesson ho to throw (UI par popup aayega)."""
    prev_lesson = validate_course_progress(doc.course, doc.lesson, doc.member)

    if prev_lesson:
        prev_title = frappe.db.get_value("Course Lesson", prev_lesson, "title") or prev_lesson
        frappe.throw(
            f"Pehle '{prev_title}' lesson complete karein.",
            frappe.PermissionError,
        )
 
 

from lms.lms.utils import get_course_details as original_get_course_details


def fetch_course_skills(course: str):
    """Helper (whitelisted nahi): custom_course_skills se skill_name aur rating."""
    rows = frappe.get_all(
        "Courses Skills",  # child doctype ka asli naam
        filters={
            "parent": course,
            "parenttype": "LMS Course",
            "parentfield": "custom_course_skills",
        },
        fields=["skill_name", "rating"],
        order_by="idx",
        parent_doctype="LMS Course",
        ignore_permissions=True,
    )
    return [r for r in rows if r.get("skill_name")]


def skill_label(r):
    return f"{r.skill_name} ({r.rating})" if r.rating else r.skill_name


@frappe.whitelist(allow_guest=True)
def get_course_skills(course: str):
    rows = fetch_course_skills(course)
    return {
        "skills": rows,
        "skills_text": ", ".join(skill_label(r) for r in rows),
    }


def rating_to_stars(rating) -> int:
    """Frappe Rating field (0 se 1) ko 5 me se stars me badalta hai."""
    try:
        value = float(rating or 0)
    except (TypeError, ValueError):
        return 0
    if value > 1:  # agar rating pehle se 1-5 scale me ho
        return min(round(value), 5)
    return round(value * 5)


def skill_label(r):
    stars = rating_to_stars(r.rating)
    return f"{r.skill_name} ({stars}/5)" if stars else r.skill_name


def build_skills_table(rows) -> str:
    body = ""
    for r in rows:
        stars = rating_to_stars(r.rating)
        star_html = (
            f'<span style="color:#f5b301;letter-spacing:2px;">{"★" * stars}</span>'
            f'<span style="opacity:.3;letter-spacing:2px;">{"★" * (5 - stars)}</span>'
        )
        percent = stars * 20
        bar_html = (
            '<div style="background:rgba(128,128,128,.25);border-radius:999px;'
            'height:6px;width:100%;min-width:80px;">'
            f'<div style="background:#22c55e;height:6px;border-radius:999px;width:{percent}%;"></div>'
            "</div>"
        )
        body += (
            "<tr>"
            f'<td style="padding:10px 12px;border-bottom:1px solid rgba(128,128,128,.25);">'
            f"{frappe.utils.escape_html(r.skill_name)}</td>"
            f'<td style="padding:10px 12px;border-bottom:1px solid rgba(128,128,128,.25);white-space:nowrap;">'
            f"{star_html} <small style='opacity:.7;'>{stars}/5</small></td>"
            f'<td style="padding:10px 12px;border-bottom:1px solid rgba(128,128,128,.25);width:30%;">'
            f"{bar_html}</td>"
            "</tr>"
        )

    return (
        '<h3 style="margin-top:24px;">Skills you will learn</h3>'
        '<table style="width:100%;border-collapse:collapse;margin-top:8px;'
        'border:1px solid rgba(128,128,128,.25);border-radius:8px;">'
        "<thead><tr>"
        '<th style="text-align:left;padding:10px 12px;border-bottom:1px solid rgba(128,128,128,.4);">Skill</th>'
        '<th style="text-align:left;padding:10px 12px;border-bottom:1px solid rgba(128,128,128,.4);">Rating</th>'
        '<th style="text-align:left;padding:10px 12px;border-bottom:1px solid rgba(128,128,128,.4);">Level</th>'
        "</tr></thead>"
        f"<tbody>{body}</tbody></table>"
    )


@frappe.whitelist(allow_guest=True)
def get_course_details_with_skills(course: str):
    data = original_get_course_details(course)
    if not isinstance(data, dict):
        return data

    rows = fetch_course_skills(course)
    data["skills"] = rows
    data["skills_text"] = ", ".join(skill_label(r) for r in rows)

    if rows:
        data["description"] = (data.get("description") or "") + build_skills_table(rows)

    return data



# @frappe.whitelist(allow_guest=True)
# def get_course_details_with_skills(course: str):
# 	data = original_get_course_details(course)
# 	if not isinstance(data, dict):
# 		return data

# 	rows = fetch_course_skills(course)

# 	data["skills"] = rows
# 	data["skills_text"] = ", ".join(skill_label(r) for r in rows)
# 	# frappe.throw(str(rows))
# 	if rows:
# 		data["description"] = (data.get("description") or "") + build_skills_table(rows)

# 	# Similar courses table (matched with the logged-in user's skills)
# 	try:
# 		similar_html = get_similar_courses_list(course=course, limit=6).get("html")
# 		if similar_html:
# 			data["description"] = (data.get("description") or "") + similar_html
# 	except Exception:
# 		frappe.log_error(
# 			title="Similar courses table failed",
# 			message=frappe.get_traceback(),
# 		)

# 	return data



import inspect

import frappe
from lms.lms.utils import get_courses



COURSE_SKILLS_FIELD = "custom_course_skills"


def _skill_names(skills) -> set:
	"""Normalize skills (list of dicts or strings) into a set of lowercase names."""
	names = set()
	for s in skills or []:
		name = s.get("skill") if isinstance(s, dict) else s
		if name:
			names.add(str(name).strip().lower())
	return names


@frappe.whitelist()
def get_similar_courses():
	"""Return LMS courses whose skills match the skills of the session user's designation."""

	user = frappe.session.user

	try:
		# 1. Skills of the user, from the HRMS API
		department, designation, skills, goals = get_employee_dept_designation(user)
		user_skills = _skill_names(skills)

		# frappe.throw(str(user_skills))

		if not user_skills:
			return []

		# 2. All courses from the LMS API
		params = inspect.signature(get_courses).parameters

		# frappe.throw(str(params))

		kwargs = {}

		if "filters" in params:
			kwargs["filters"] = {}

		if "start" in params:
			kwargs["start"] = 0

		if "page_length" in params:
			kwargs["page_length"] = 1000

		courses = get_courses(**kwargs) or []

		if not courses:
			return []

		# 2b. Remove the courses the user is already enrolled in
		enrolled_courses = set(
			frappe.get_all(
				"LMS Enrollment",
				filters={"member": user},
				pluck="course",
			)
		)
  
		# frappe.throw(f"{enrolled_courses, user}")

		courses = [
			c
			for c in courses
			if c.get("name") not in enrolled_courses
		]

		if not courses:
			return []

		# 3. Child doctype and skill field
		table_field = frappe.get_meta("LMS Course").get_field(
			COURSE_SKILLS_FIELD
		)

		# frappe.throw(str(table_field))

		if not table_field:
			frappe.throw(
				f"LMS Course has no field named '{COURSE_SKILLS_FIELD}'"
			)

		child_doctype = table_field.options
		child_meta = frappe.get_meta(child_doctype)

		skill_field = None

		for f in child_meta.fields:
			if f.fieldtype == "Link" and f.options == "Skill":
				skill_field = f.fieldname
				break

		if not skill_field:
			for f in child_meta.fields:
				if f.fieldname == "skill":
					skill_field = f.fieldname
					break

		if not skill_field:
			for f in child_meta.fields:
				if f.fieldtype in ("Link", "Data"):
					skill_field = f.fieldname
					break

		if not skill_field:
			frappe.throw(
				f"Skill field not found in {child_doctype}"
			)

		# 4. Fetch the skills of all courses in one query
		course_names = [
			c.get("name")
			for c in courses
			if c.get("name")
		]

		# frappe.throw(f"{course_names}")

		if not course_names:
			return []

		rows = frappe.get_all(
			child_doctype,
			filters={
				"parent": ["in", course_names],
				"parenttype": "LMS Course",
				"parentfield": COURSE_SKILLS_FIELD,
			},
			fields=[
				"parent",
				skill_field,
			],                                                                                                                                                                 
		)

		# frappe.throw(f"{rows}")

		course_skills = {}

		for r in rows:
			value = r.get(skill_field)

			if value:
				course_skills.setdefault(
					r.parent,
					set()
				).add(
					str(value).strip().lower()
				)

		# 5. Match user skills with course skills
		result = []

		for c in courses:

			matched = (
				user_skills
				& course_skills.get(
					c.get("name"),
					set()
				)
			)

			if matched:
				c["matched_skills"] = sorted(matched)
				c["match_count"] = len(matched)
				result.append(c)

		# Sort by best matchsa
		result.sort(
			key=lambda c: c["match_count"],
			reverse=True
		)
  
		# frappe.throw(f"{result}")

		return result

	except Exception:
		frappe.log_error(
			title="get_similar_courses failed",
			message=frappe.get_traceback(),
		)

		frappe.throw(
			frappe.get_traceback()
		)


def build_similar_courses_table(courses) -> str:
	max_count = max(
		(c.get("match_count") or 1) for c in courses
	) if courses else 1

	body = ""

	for c in courses:
		name = frappe.utils.escape_html(c.get("name") or "")
		title = frappe.utils.escape_html(
			c.get("title") or c.get("name") or ""
		)

		skills = ", ".join(
			frappe.utils.escape_html(s)
			for s in c.get("matched_skills", [])
		)

		count = c.get("match_count") or 1
		percent = round(count / max_count * 100)

		bar_html = (
			'<div style="background:rgba(128,128,128,.25);'
			'border-radius:999px;height:6px;width:100%;min-width:80px;">'
			f'<div style="background:#22c55e;height:6px;'
			f'border-radius:999px;width:{percent}%;"></div>'
			"</div>"
		)

		body += (
			"<tr>"
			f'<td style="padding:10px 12px;'
			f'border-bottom:1px solid rgba(128,128,128,.25);">'
			f'<a href="/lms/courses/{name}" '
			f'style="text-decoration:none;">{title}</a></td>'

			f'<td style="padding:10px 12px;'
			f'border-bottom:1px solid rgba(128,128,128,.25);">'
			f"{skills}</td>"

			f'<td style="padding:10px 12px;'
			f'border-bottom:1px solid rgba(128,128,128,.25);width:30%;">'
			f"{bar_html}</td>"

			"</tr>"
		)

	return (
		'<h3 style="margin-top:24px;">Similar Courses</h3>'
		'<table style="width:100%;border-collapse:collapse;margin-top:8px;'
		'border:1px solid rgba(128,128,128,.25);border-radius:8px;">'

		"<thead><tr>"
		'<th style="text-align:left;padding:10px 12px;'
		'border-bottom:1px solid rgba(128,128,128,.4);">'
		"Course</th>"

		'<th style="text-align:left;padding:10px 12px;'
		'border-bottom:1px solid rgba(128,128,128,.4);">'
		"Matching Skills</th>"

		'<th style="text-align:left;padding:10px 12px;'
		'border-bottom:1px solid rgba(128,128,128,.4);">'
		"Match</th>"

		"</tr></thead>"

		f"<tbody>{body}</tbody>"
		"</table>"
	)
 
 
 
import frappe

LINK_ID = "similar-courses-link"

LINK_HTML = (
	f'<a id="{LINK_ID}" href="/similar-courses" '
	'style="position:fixed;top:9px;right:20px;z-index:9999;'
	'padding:6px 14px;border-radius:6px;'
	'border:1px solid rgba(128,128,128,.4);'
	'background:rgba(128,128,128,.18);color:inherit;'
	'font-size:13px;font-weight:600;text-decoration:none;">'
	'Similar Courses &rarr;</a>'
)


def add_link(response=None, request=None, **kwargs):
	try:
		if response is None or request is None:
			return

		path = request.path or ""

		if not path.startswith("/lms"):
			return

		if response.status_code != 200:
			return

		if response.mimetype != "text/html":
			return

		if getattr(response, "direct_passthrough", False):
			return

		html = response.get_data(as_text=True)

		if "</body>" not in html:
			return

		if LINK_ID in html:
			return

		response.set_data(
			html.replace(
				"</body>",
				LINK_HTML + "</body>",
				1
			)
		)

	except Exception:
		frappe.log_error(
			title="Similar courses link inject failed",
			message=frappe.get_traceback(),
		)
  
  
  
  
  
import frappe
from frappe import _
from frappe.utils import flt, get_url_to_form

DEFAULT_THRESHOLD = 40  # percent: a goal score below this triggers a Performance Improvement Plan


import requests
import frappe

DEFAULT_THRESHOLD = 5

@frappe.whitelist(allow_guest=True)
def calculate_goal_score(user_id: str | None = None) -> dict:
    try:
        user_id = user_id or frappe.session.user

        if not user_id or user_id == "Guest":
            return {
                "success": False,
                "message": "Valid user_id is required."
            }

        url = (
            "http://ec2-13-234-27-130.ap-south-1.compute.amazonaws.com:8001"
            "/api/method/get_employee_apprisal"
        )

        response = requests.get(
            url,
            params={"user_id": user_id},
            timeout=30,
        )
        response.raise_for_status()

        result = response.json().get("message", {})
        appraisals = result.get("appraisals", [])

        if not result.get("success") or not appraisals:
            return {
                "success": False,
                "message": "Appraisal not found",
                "result": result,
            }

        total_score = appraisals[0].get("total_score")

        if total_score is None:
            return {
                "success": False,
                "message": "Total score not found",
            }

        total_score = float(total_score)

        if total_score < DEFAULT_THRESHOLD:

            check_already_created_pip = frappe.db.exists(
                "Performance Improvement Plan",
                {"user_id": user_id}
            )

            if not check_already_created_pip:
                employee_name = (
                    frappe.db.get_value("User", user_id, "full_name")
                    or frappe.db.get_value("User", user_id, "first_name")
                    or user_id
                )

                pip = frappe.get_doc({
                    "doctype": "Performance Improvement Plan",
                    "user_id": user_id,
                    "employee_name": employee_name,
                    "reason": (
                        f"Goal score is {total_score}%, "
                        f"below the required {DEFAULT_THRESHOLD}%."
                    ),
                })

                pip.insert(ignore_permissions=True)

                # Explicitly commit the database transaction
                frappe.db.commit()

                # Verify the saved document and its fields
                saved_pip = frappe.db.get_value(
                    "Performance Improvement Plan",
                    pip.name,
                    ["name", "user_id", "employee_name", "reason"],
                    as_dict=True
                )

                if not saved_pip:
                    return {
                        "success": False,
                        "message": "PIP record was not found after saving.",
                        "pip_name": pip.name,
                    }

                return {
                    "success": True,
                    "pip_created": True,
                    "pip_name": saved_pip.name,
                    "saved_in_db": True,
                    "user_id": saved_pip.user_id,
                    "employee_name": saved_pip.employee_name,
                    "reason": saved_pip.reason,
                    "total_score": total_score,
                    "threshold": DEFAULT_THRESHOLD,
                    "result": result,
                    "message": "PIP saved and verified successfully.",
                }

        return {
            "success": True,
            "pip_created": False,
            "total_score": total_score,
            "threshold": DEFAULT_THRESHOLD,
            "result": result,
            "message": "Score threshold ke barabar ya usse zyada hai.",
        }

    except requests.RequestException:
        frappe.log_error(
            title="Calculate Goal Score API Error",
            message=frappe.get_traceback(),
        )
        return {
            "success": False,
            "message": "Unable to fetch appraisal data from the API.",
        }

    except Exception:
        frappe.log_error(
            title="Calculate Goal Score Error",
            message=frappe.get_traceback(),
        )
        return {
            "success": False,
            "message": "An error occurred while calculating the goal score.",
        }

def create_pip_and_notify(user, employee_name, score_percent, threshold, appraisal_cycle):
	"""Trigger: create the Performance Improvement Plan and mail the employee."""
	marker = f"[Auto PIP: {appraisal_cycle}]"

	# One automatic PIP per employee per cycle
	existing = frappe.db.exists(
		"Performance Improvement Plan",
		{
			"employee_id": user,
			"docstatus": ["<", 2],
			"reason": ["like", f"%{marker}%"],
		},
	)
	if existing:
		return {"pip": existing, "created": False, "mail_sent": False}

	pip = frappe.get_doc({
		"doctype": "Performance Improvement Plan",
		"employee_id": user,
		"employee_name": employee_name,
		"reason": (
			f"{marker} Goal score is {score_percent}%, below the required {threshold}% "
			f"for the appraisal cycle {appraisal_cycle}."
		),
	})
	pip.insert(ignore_permissions=True)

	if SUBMIT_PIP:
		pip.submit()

	mail_sent = send_pip_mail(
		user, employee_name, score_percent, threshold, appraisal_cycle, pip.name
	)

	return {"pip": pip.name, "created": True, "mail_sent": mail_sent}


# muje User doc use krna h Employee nhi use krna h





# added commit

import frappe
import requests


SKILLS_GRADE_API = (
    "http://ec2-13-234-27-130.ap-south-1.compute.amazonaws.com:8001/api/method/get_user_skills_grade_for_lms"
)



@frappe.whitelist(allow_guest=True)
def validate_enrolled_course_skills(user: str | None = None):
    user = user or frappe.session.user

    if not user or user == "Guest":
        frappe.throw("Please login first")

    # 1. Fetch skills and ratings from external API
    try:
        response = requests.get(
            SKILLS_GRADE_API,
            params={"user_id": user},
            timeout=15,
        )
        response.raise_for_status()
        api_response = response.json().get("message", {})

    except requests.RequestException as e:
        frappe.throw(f"Skills grade API request failed: {str(e)}")

    if api_response.get("status") != "success":
        frappe.throw("Skills grade API did not return success.")

    # 2. Build rating map
    user_skill_ratings = {}

    for feedback in api_response.get("data", []):
        for skill_row in feedback.get("custom_skills_grade", []):
            skill_name = skill_row.get("skills")
            rating = skill_row.get("rating")

            if skill_name and rating is not None:
                key = skill_name.strip().lower()

                user_skill_ratings[key] = max(
                    user_skill_ratings.get(key, float("-inf")),
                    float(rating),
                )

    if not user_skill_ratings:
        return {
            "success": True,
            "user": user,
            "skills_received": [],
            "matched_courses": [],
            "message": "No skill ratings found in the API response.",
        }

    # 3. Fetch all LMS Courses
    courses = frappe.get_all(
        "LMS Course",
        fields=["name", "title"],
    )

    matched_courses = []
    

    for course_row in courses:
        course_doc = frappe.get_doc("LMS Course", course_row.name)
        course_skills = course_doc.get("custom_course_skills") or []

        matched_skills = []
        low_skills = []
        has_matching_skill = False

        for course_skill in course_skills:
            skill_name = (
                course_skill.get("skills")
                or course_skill.get("skill")
                or course_skill.get("skill_name")
            )

            required_rating = (
                course_skill.get("rating")
                if course_skill.get("rating") is not None
                else course_skill.get("required_rating")
            )

            if not skill_name:
                continue

            skill_key = skill_name.strip().lower()

            if skill_key not in user_skill_ratings:
                continue

            has_matching_skill = True
            user_rating = user_skill_ratings[skill_key]

            if required_rating is None:
                matched_skills.append({
                    "skill": skill_name,
                    "user_rating": user_rating,
                    "required_rating": None,
                    "status": "matched",
                })
                continue

            required_rating = float(required_rating)

            skill_result = {
                "skill": skill_name,
                "user_rating": user_rating,
                "required_rating": required_rating,
                "status": (
                    "low"
                    if user_rating < required_rating
                    else "matched"
                ),
            }

            matched_skills.append(skill_result)

            if user_rating < required_rating:
                low_skills.append(skill_result)

        if has_matching_skill:
            matched_courses.append({
                "course": course_doc.name,
                "title": course_row.title,
                "matched_skills": matched_skills,
                "low_skills": low_skills,
                "has_low_scores": bool(low_skills),
            })
            
    # frappe.throw(f"{user_rating}")
    # 4. Enroll the user in the matching course, if not already enrolled
    if matched_courses:
        
        data = get_similar_courses()

        if data:
            
            for matched_course in matched_courses:
                
                if matched_course.get("course") == data[0].name and matched_course.get("has_low_scores") is False:
                    
                    course_name = matched_course.get("course")

                    # Avoid duplicate enrollment
                    if not frappe.db.exists(
                        "LMS Enrollment",
                        {
                            "member": user,
                            "course": course_name,
                        },
                    ):
                        enrollment = frappe.get_doc({
                            "doctype": "LMS Enrollment",
                            "member": user,
                            "course": course_name,
                            "member_type": "Student",
                        })

                        enrollment.insert(ignore_permissions=True)

    return {
        "success": True,
        "user": user,
        "skills_received": [
            {"skill": skill, "rating": rating}
            for skill, rating in user_skill_ratings.items()
        ],
        "total_courses_checked": len(courses),
        "total_matched_courses": len(matched_courses),
        "matched_courses": matched_courses,
        "message": "Courses matched with API skills successfully.",
    }