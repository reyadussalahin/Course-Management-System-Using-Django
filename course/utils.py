from . import restrictions
import secrets

from course.models import Course
from course.models import Instructor
from course.models import Student


def generate_key():
	random_generator = secrets.SystemRandom()
	password = ''.join(random_generator.choice(restrictions.COURSE_KEY_CHAR_LIST) for i in range(restrictions.COURSE_KEY_LEN))
	return password

def check_is_instructor(course, instructor):
	return Instructor.objects.filter(
			course=course,
			instructor=instructor).exists()

def check_is_student(course, student):
	return Student.objects.filter(
		course=course,
		student=student).exists()

def check_is_creator(course, creator):
	return Course.objects.filter(
		creator=creator,
		course_name=course.course_name,
		session_name=course.session_name).exists()

