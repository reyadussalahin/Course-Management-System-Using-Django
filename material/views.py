from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import Http404
from django.core.urlresolvers import reverse

from course.models import Course
from course.models import Instructor
from course.models import Student

from course.utils import check_is_student
from course.utils import check_is_instructor
from course.utils import check_is_creator

from material.models import Topic
from material.models import Material

from material.forms import TopicForm
from material.forms import MaterialForm


from course_management import settings


def topic_list(request, course_id):
	try:
		course = Course.objects.get(id=course_id)
	except Course.DoesNotExist:
		raise Http404('course with provided request does not exist')

	# have to provide a message
	# if user is not a student, instructor, or creator of this course
	# i'll do it later

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

	topic_list = Topic.objects.filter(course=course).order_by('topic_serial')
	is_instructor = check_is_instructor(course, request.user)
	context = {
		'course' : course,
		'topic_list' : topic_list,
		'is_instructor' : is_instructor,
	}

	return render(request, 'material/topic_list.html', context=context)



def add_topic(request, course_id):
	# if settings.DEBUG:
	# 	print('is_authenticated: {}'.format(request.user.is_authenticated()))
	
	# if not request.user.is_authenticated():
	# 	return HttpResponseRedirect(reverse('login'))

	try:
		course = Course.objects.get(id=course_id)
	except Course.DoesNotExist:
		raise Http404('course with provided request does not exist')

	# have to provide a message
	# if user is not an instructor of this course
	# becuase only instructor can add materials
	# even creator or student cant do it..so..
	# i'll do it later

	if request.user.is_authenticated():
		is_ok = check_is_instructor(course, request.user)
	else:
		is_ok = False

	if not is_ok:
		message = 'The only people have access to view this page is the instructor of this course'
		context = {
			'message' : message,
		}
		return render(request, 'unauthorized.html', context=context)
	 
	if request.method == 'POST':
		topic_form = TopicForm(request.POST, course=course)

		if topic_form.is_valid():
			topic = topic_form.save(commit=False)

			topic_count = Topic.objects.filter(course=course).count()
			
			if topic.topic_serial and topic.topic_serial <= topic_count:
				for topic_obj in Topic.objects.filter(
					course=course,
					topic_serial__gte=topic.topic_serial):
					topic_obj.topic_serial = topic_obj.topic_serial + 1
					topic_obj.updater = request.user
					topic_obj.save()
			else:
				topic.topic_serial = topic_count + 1

			topic.creator = request.user
			topic.updater = request.user
			topic.course = course
			topic.save()

			kwargs = {
				'course_id' : course.id,
			}

			return HttpResponseRedirect(reverse('topic_list', kwargs=kwargs))
		else:
			print(topic_form.errors)
	else:
		topic_form = TopicForm(course=course)

	context = {
		'course' : course,
		'form' : topic_form,
	}

	return render(request, 'material/add_topic.html', context=context)


def material_list(request, topic_id):
	try:
		topic = Topic.objects.get(id=topic_id)
	except Topic.DoesNotExist:
		raise Http404('topic with provided request does not exist')

	course = topic.course
	# have to provide a message
	# if user is not an instructor of this course
	# becuase only instructor can add materials
	# even creator or student cant do it..so..
	# i'll do it later...done it actually...see below codes
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
	
	material_list = Material.objects.filter(topic=topic)
	is_instructor = check_is_instructor(course, request.user)
	context = {
		'course' : course,
		'topic' : topic,
		'material_list' : material_list,
		'is_instructor' : is_instructor,
	}

	return render(request, 'material/material_list.html', context=context)


def add_material(request, topic_id):
	try:
		topic = Topic.objects.get(id=topic_id)
	except Topic.DoesNotExist:
		raise Http404('topic with provided request does not exist')

	course = topic.course
	# have to provide a message
	# if user is not an instructor of this course
	# becuase only instructor can add materials
	# even creator or student cant do it..so..
	# i'll do it later...done it actually...see below codes
	if request.user.is_authenticated():
		is_ok = check_is_instructor(course, request.user)
	else:
		is_ok = False

	if not is_ok:
		message = 'The only people have access to view this page is the instructor of this course'
		context = {
			'message' : message,
		}
		return render(request, 'unauthorized.html', context=context)
	
	if request.method == 'POST':
		material_form = MaterialForm(request.POST, request.FILES, topic=topic)
		if material_form.is_valid():
			material = material_form.save(commit=False)

			material_count = Material.objects.filter(topic=topic).count()
			material.material_serial = material_count + 1
			material.creator = request.user
			material.updater = request.user
			material.topic = topic

			material.save()
			kwargs = {
				'topic_id' : topic.id,
			}
			return HttpResponseRedirect(reverse('material_list', kwargs=kwargs))
		else:
			print(material_form.errors)
	else:
		material_form = MaterialForm(topic=topic)
	
	context = {
		'course' : course,
		'topic' : topic,
		'form' : material_form,
	}
	return render(request, 'material/add_material.html', context=context)
