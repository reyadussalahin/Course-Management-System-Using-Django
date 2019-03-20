from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import Http404
from django.core.urlresolvers import reverse

from course.models import Course
from course.forms import Instructor
from course.models import Student

from course.forms import CourseForm
from course.forms import InstructorForm
from course.forms import StudentForm

from course.utils import generate_key
from course.utils import check_is_student
from course.utils import check_is_instructor
from course.utils import check_is_creator

from course_management import settings

def course_list(request, username):
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		raise Http404('user does not exist')

	course_created = Course.objects.filter(creator=user)
	course_enrolled = []
	for student_info in Student.objects.filter(student=user):
		course_enrolled.append(student_info.course)
		if settings.DEBUG:
			print(student_info.course)

	course_instructed = []
	for instructor_info in Instructor.objects.filter(instructor=user):
		course_instructed.append(instructor_info.course)

	bar_before_instructed = course_created and course_instructed
	bar_before_enrolled = (course_created or course_instructed) and course_enrolled
	context = {
		'username' : username,
		'course_created' : course_created,
		'course_enrolled' : course_enrolled,
		'course_instructed' : course_instructed,
		'bar_before_enrolled' : bar_before_enrolled,
		'bar_before_instructed' : bar_before_instructed,
	}

	return render(request, 'course/course_list.html', context=context)



def create_course(request):
	if settings.DEBUG:
		print('is_authenticated: {}'.format(request.user.is_authenticated()))
	
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))

	if request.method == 'POST':
		course_form = CourseForm(request.POST, user=request.user)
		if course_form.is_valid():
			course = course_form.save(commit=False)

			course.creator = request.user

			student_key = generate_key()
			while Course.objects.filter(student_key=student_key).exists():
				student_key = generate_key()
			
			course.student_key = student_key
			
			instructor_key = generate_key()
			while Course.objects.filter(instructor_key=instructor_key).exists():
				instructor_key = generate_key()

			course.instructor_key = instructor_key

			course.save()
			kwargs = {
				'username' : request.user.username
			}
			return HttpResponseRedirect(reverse('course_list', kwargs=kwargs))
		else:
			print(course_form.errors)
	else:
		course_form = CourseForm(user=request.user)

	context = {
		'form' : course_form,
	}
	return render(request, 'course/create_course.html', context=context)




def instruct_course(request):
	if settings.DEBUG:
		print('is_authenticated: {}'.format(request.user.is_authenticated()))

	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))

	if request.method == 'POST':
		instructor_form = InstructorForm(request.POST, user=request.user)
		print('instructor form: {}'.format(instructor_form))

		if instructor_form.is_valid():
			instructor = instructor_form.save(commit=False)

			instructor.instructor = request.user
			try:
				instructor_key = instructor_form.cleaned_data.get('instructor_key', None)
				instructor.course = Course.objects.get(instructor_key=instructor_key)
			except Course.DoesNotExist:
				return Http404('course with provided key does not exist')

			instructor.save()
			
			if settings.DEBUG:
				print(instructor)

			kwargs = {
				'username' : request.user.username
			}
			return HttpResponseRedirect(reverse('course_list', kwargs=kwargs))
		else:
			print(instructor_form.errors)
	else:
		instructor_form = InstructorForm(user=request.user)

	context = {
		'form' : instructor_form,
	}
	return render(request, 'course/instruct_course.html', context=context)



def enroll_course(request):
	if settings.DEBUG:
		print('is_authenticated: {}'.format(request.user.is_authenticated()))

	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))

	if request.method == 'POST':
		student_form = StudentForm(request.POST, user=request.user)
		print('student form: {}'.format(student_form))

		if student_form.is_valid():
			student = student_form.save(commit=False)

			student.student = request.user
			try:
				student_key = student_form.cleaned_data.get('student_key', None)
				student.course = Course.objects.get(student_key=student_key)
			except Course.DoesNotExist:
				return Http404('course with provided key does not exist')

			student.save()
			
			if settings.DEBUG:
				print(student)

			kwargs = {
				'username' : request.user.username
			}
			return HttpResponseRedirect(reverse('course_list', kwargs=kwargs))
		else:
			print(student_form.errors)
	else:
		student_form = StudentForm(user=request.user)

	context = {
		'form' : student_form,
	}
	return render(request, 'course/enroll_course.html', context=context)



def course_index(request, course_id):
	try:
		course = Course.objects.get(id=course_id)
	except Course.DoesNotExist:
		raise Http404('course with provided request deos not exist')

	if request.user.is_authenticated():
		is_ok = check_is_creator(course,
			request.user) or check_is_instructor(course,
			request.user) or check_is_student(course,
			request.user)
	else:
		is_ok = False
	
	context = {
		'course' : course,
		'is_ok' : is_ok,
	}

	return render(request, 'course/course_index.html', context=context)


def student_list(request, course_id):
	try:
		course = Course.objects.get(id=course_id)
	except Course.DoesNotExist:
		raise Http404('course with provided request does not exist')

	# we've to provide a message here if someone is not logged in as
	# a student, intructor or creator...because only this 3 type of person
	# can see student data
	# so if anyone is logged in as such
	# redirect them to a page telling them that only creator, instructor
	# or student can only see this data
	# it's not written yet

	if request.user.is_authenticated():
		is_ok = check_is_creator(course,
			request.user) or check_is_instructor(course,
			request.user) or check_is_student(course,
			request.user)
	else:
		is_ok = False

	if not is_ok:
		message = 'The only people have access to view this page is the students, instructors or creator of this course'
		context = {
			'message' : message,
		}
		return render(request, 'unauthorized.html', context=context)
		
	student_list = Student.objects.filter(course=course).order_by('class_id')

	context = {
		'course' : course,
		'student_list' : student_list,
	}

	return render(request, 'course/student_list.html', context=context)

def instructor_list(request, course_id):
	try:
		course = Course.objects.get(id=course_id)
	except Course.DoesNotExist:
		raise Http404('course with provided request does not exist')

	# we dont have to provide a message here
	# because anyone can see instructors of a course
	
	instructor_list = Instructor.objects.filter(course=course)

	context = {
		'course' : course,
		'instructor_list' : instructor_list,
	}

	return render(request, 'course/instructor_list.html', context=context)

