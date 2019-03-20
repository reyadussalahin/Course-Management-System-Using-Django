import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course_management.settings')

import django
django.setup()

from django.contrib.auth.models import User
from registration.models import UserProfile
from course.models import Course
from course.models import Student
from course.models import Instructor

from django.core.files import File
from django.core.files.images import ImageFile
from course.utils import generate_key

from django.db import IntegrityError


user_list = [
	{
		'first_name' : 'Albus',
		'last_name' : 'Dumbledoor',
		'username' : 'albus',
		'email' : 'albus@gmail.com',
		'password' : '12345678',
		'picture' : 'images/albus.jpg',
	},
	
	{
		'first_name' : 'Bellatrix',
		'last_name' : 'Lestrange',
		'username' : 'bella',
		'email' : 'bella@gmail.com',
		'password' : '12345678',
		'picture' : 'images/bella.jpg',
	},

	{
		'first_name' : 'Cho',
		'last_name' : 'Chang',
		'username' : 'cho',
		'email' : 'cho@gmail.com',
		'password' : '12345678',
		'picture' : 'images/cho.jpg',
	},

	{
		'first_name' : 'Draco',
		'last_name' : 'Malfoy',
		'username' : 'draco',
		'email' : 'draco@gmail.com',
		'password' : '12345678',
		'picture' : 'images/draco.jpg',
	},

	{
		'first_name' : 'Fleur',
		'last_name' : 'Delacour',
		'username' : 'fleur',
		'email' : 'fleur@gmail.com',
		'password' : '12345678',
		'picture' : 'images/fleur.png',
	},

	{
		'first_name' : 'Fred',
		'last_name' : 'Wisley',
		'username' : 'fred',
		'email' : 'fred@gmail.com',
		'password' : '12345678',
		'picture' : 'images/fred.jpg',
	},

	{
		'first_name' : 'George',
		'last_name' : 'Wisley',
		'username' : 'george',
		'email' : 'george@gmail.com',
		'password' : '12345678',
		'picture' : 'images/george.jpg',
	},

	{
		'first_name' : 'Ginny',
		'last_name' : 'Wisley',
		'username' : 'ginny',
		'email' : 'ginny@gmail.com',
		'password' : '12345678',
		'picture' : 'images/ginny.jpg',
	},

	{
		'first_name' : 'Hermione',
		'last_name' : 'Granger',
		'username' : 'hermione',
		'email' : 'hermione@gmail.com',
		'password' : '12345678',
		'picture' : 'images/hermione.jpg',
	},

	{
		'first_name' : 'Hogwarts',
		'last_name' : 'School',
		'username' : 'hogwarts',
		'email' : 'hogwarts@gmail.com',
		'password' : '12345678',
		'picture' : 'images/hogwarts.jpg',
	},

	{
		'first_name' : 'Luna',
		'last_name' : 'Lovegood',
		'username' : 'luna',
		'email' : 'luna@gmail.com',
		'password' : '12345678',
		'picture' : 'images/luna.jpeg',
	},

	{
		'first_name' : 'Minerva',
		'last_name' : 'Macgonnagol',
		'username' : 'minerva',
		'email' : 'minerva@gmail.com',
		'password' : '12345678',
		'picture' : 'images/minerva.jpg',
	},

	{
		'first_name' : 'Neville',
		'last_name' : 'Longbottom',
		'username' : 'neville',
		'email' : 'neville@gmail.com',
		'password' : '12345678',
		'picture' : 'images/neville.jpg',
	},

	{
		'first_name' : 'Padma',
		'last_name' : 'Patil',
		'username' : 'padma',
		'email' : 'padma@gmail.com',
		'password' : '12345678',
		'picture' : 'images/padma.jpg',
	},

	{
		'first_name' : 'Pansy',
		'last_name' : 'Parkinson',
		'username' : 'parkinson',
		'email' : 'parkinson@gmail.com',
		'password' : '12345678',
		'picture' : 'images/parkinson.jpg',
	},

	{
		'first_name' : 'Parvati',
		'last_name' : 'Patil',
		'username' : 'parvati',
		'email' : 'parvati@gmail.com',
		'password' : '12345678',
		'picture' : 'images/parvati.jpg',
	},

	{
		'first_name' : 'Harry',
		'last_name' : 'Potter',
		'username' : 'potter',
		'email' : 'potter@gmail.com',
		'password' : '12345678',
		'picture' : 'images/potter.jpg',
	},

	{
		'first_name' : 'Ron',
		'last_name' : 'Wisley',
		'username' : 'ron',
		'email' : 'ron@gmail.com',
		'password' : '12345678',
		'picture' : 'images/ron.jpg',
	},

	{
		'first_name' : 'Severus',
		'last_name' : 'Snape',
		'username' : 'severus',
		'email' : 'severus@gmail.com',
		'password' : '12345678',
		'picture' : 'images/severus.jpg',
	},

	{
		'first_name' : 'Sirius',
		'last_name' : 'Black',
		'username' : 'sirius',
		'email' : 'sirius@gmail.com',
		'password' : '12345678',
		'picture' : 'images/sirius.jpg',
	},

	{
		'first_name' : 'Tom',
		'last_name' : 'Riddle',
		'username' : 'tom',
		'email' : 'tom@gmail.com',
		'password' : '12345678',
		'picture' : 'images/tom.jpg',
	},

]

def populate_users_and_user_profiles():
	for data in user_list:
		try:
			user, is_user_created = User.objects.get_or_create(
				first_name=data['first_name'],
				last_name=data['last_name'],
				username=data['username'],
				email=data['email'],
				password=data['password'])
			user.set_password(user.password)
			user.save()

			_, file_name = os.path.split(data['picture'])
			picture_file = ImageFile(open(data['picture'], 'rb'))

			user_profile, is_profile_created = UserProfile.objects.get_or_create(user=user)

			user_profile.picture.save(name=file_name, content=picture_file, save=False)
			user_profile.save()
			
			print('user: {}'.format(user))

		except IntegrityError:
			print('{} already exists'.format(data['username']))


# course_list_hogwarts = [
# 	{
# 		'course_name' : 'Artificial Intelligence',
# 		'session_name' : 'Fall 2018',
# 		'start_date' : '23-07-2018',
# 	},

# 	{
# 		'course_name' : 'Discrete Math',
# 		'session_name' : 'Spring 2018',
# 		'start_date' : '12-03-2018',
# 	},

# 	{
# 		'course_name' : 'Operating System Internals',
# 		'session_name' : 'Spring 2019',
# 		'start_date' : '23-03-2019',
# 	},

# 	{
# 		'course_name' : 'Microprocessor',
# 		'session_name' : 'Fall 2018',
# 		'start_date' : '23-07-2018',
# 	},

# 	{
# 		'course_name' : 'Database',
# 		'session_name' : 'Spring 2018',
# 		'start_date' : '12-03-2018',
# 	},
# ]


course_list = [
	{
		'creator' : 'hogwarts',
		'courses' : [
			{
				'course_name' : 'Artificial Intelligence',
				'session_name' : 'Fall 2018',
				'start_date' : '2018-07-23',
			},

			{
				'course_name' : 'Discrete Math',
				'session_name' : 'Spring 2018',
				'start_date' : '2018-03-12',
			},

			{
				'course_name' : 'Operating System Internals',
				'session_name' : 'Spring 2019',
				'start_date' : '2019-03-23',
			},

			{
				'course_name' : 'Microprocessor',
				'session_name' : 'Fall 2018',
				'start_date' : '2018-07-23',
			},

			{
				'course_name' : 'Database',
				'session_name' : 'Spring 2018',
				'start_date' : '2018-03-12',
			},
		],
	},
]


def populate_courses():
	for data in course_list:
		creator = User.objects.get(username=data['creator'])
		courses = data['courses']

		for course_info in courses:
			student_key = generate_key()
			instructor_key = generate_key()
			if Course.objects.filter(
				creator=creator,
				course_name=course_info['course_name'],
				session_name=course_info['session_name']).exists():
				print('{} already exists'.format(course_info['course_name']))
			else:
				course, is_course_created = Course.objects.get_or_create(
					creator=creator,
					student_key=student_key,
					instructor_key=instructor_key,
					course_name=course_info['course_name'],
					session_name=course_info['session_name'],
					start_date=course_info['start_date'])
				course.save()
				print('course: {}'.format(course))


student_list = [
	{
		'creator' : 'hogwarts',
		'course_name' : 'Artificial Intelligence',
		'session_name' : 'Fall 2018',
		'students' : [
			{
				'name' : 'cho',
				'id' : 1404001,
			},

			{
				'name' : 'draco',
				'id' : 1404002,
			},

			{
				'name' : 'fleur',
				'id' : 1404003,
			},

			{
				'name' : 'hermione',
				'id' : 1404004,
			},

			{
				'name' : 'luna',
				'id' : 1404005,
			},

			{
				'name' : 'neville',
				'id' : 1404006,
			},

			{
				'name' : 'padma',
				'id' : 1404007,
			},

			{
				'name' : 'parvati',
				'id' : 1404008,
			},

			{
				'name' : 'parkinson',
				'id' : 1404009,
			},

			{
				'name' : 'potter',
				'id' : 1404010,
			},

			{
				'name' : 'ron',
				'id' : 1404011,
			},
		]
	},

	{
		'creator' : 'hogwarts',
		'course_name' : 'Operating System Internals',
		'session_name' : 'Spring 2019',
		'students' : [
			{
				'name' : 'fred',
				'id' : 1404001,
			},

			{
				'name' : 'george',
				'id' : 1404002,
			},

			{
				'name' : 'hermione',
				'id' : 1404003,
			},
		]
	},
]


def populate_students():
	for data in student_list:
		try:
			username = data['creator']
			creator = User.objects.get(username=username)
			course_name = data['course_name']
			session_name = data['session_name']

			print('')
			print('Course provider: {}'.format(creator.username))
			
			try:
				course = Course.objects.get(creator=creator, course_name=course_name, session_name=session_name)
				
				print('Course name: {}({})'.format(course.course_name, course.session_name))
				print('')

				for person in data['students']:
					try:
						user_student = User.objects.get(username=person['name'])
						class_id = person['id']

						if Student.objects.filter(course=course, student=user_student).exists():
							print('{} is already a student'.format(person['name']))
							continue

						if Student.objects.filter(course=course, class_id=class_id).exists():
							print('{} id is already taken'.format(person['id']))
							continue

						try:
							student, is_created = Student.objects.get_or_create(course=course,
								student=user_student,
								class_id=class_id)

							student.save()
							print('{} is added as a student'.format(user_student.username))

						except IntegrityError:
							print('cant create object...already exists')

					except User.DoesNotExist:
						print('{} does not exist'.format(person['name']))
			except Course.DoesNotExist:
				print('{} has not provided any course named {}({})'.format(username, course_name, session_name))
		except User.DoesNotExist:
			print('user not found')



instructor_list = [
	{
		'creator' : 'hogwarts',
		'course_name' : 'Operating System Internals',
		'session_name' : 'Spring 2019',
		'instructors' : [ 'severus', 'minerva', ],
	},

	{
		'creator' : 'hogwarts',
		'course_name' : 'Artificial Intelligence',
		'session_name' : 'Fall 2018',
		'instructors' : [ 'albus', ]
	},
]


def populate_instructors():
	for data in instructor_list:
		try:
			creator = User.objects.get(username=data['creator'])
			print('')
			print('Course provider: {}'.format(creator.username))
			try:
				course = Course.objects.get(
					creator=creator,
					course_name=data['course_name'],
					session_name=data['session_name'])
				print('Course name: {}({})'.format(course.course_name, course.session_name))
				print('')
				for instructor_name in data['instructors']:
					try:
						instructor = User.objects.get(username=instructor_name)
						if Instructor.objects.filter(course=course, instructor=instructor).exists():
							print('{} is already an instructor'.format(instructor.username))
							continue
						try:
							instructor_info, is_created = Instructor.objects.get_or_create(
								course=course,
								instructor=instructor)
							instructor_info.save()
							print('{} is added as an instructor'.format(instructor.username))
						except IntegrityError:
							print('cant create object...already exists')

					except User.DoesNotExist:
						print('{} does not exist'.format(instructor_name))
			except Course.DoesNotExist:
				print('{} has not provided any course named {}({})'.format(username, course_name, session_name))
		except User.DoesNotExist:
			print('user not found')



if __name__ == '__main__':
	print('running population_script...')
	print('populating users...')
	populate_users_and_user_profiles()
	print('user population done...')
	print('')
	print('populating courses...')
	populate_courses()
	print('course population done...')
	print('')
	print('populating students...')
	populate_students()
	print('student population done...')
	print('')
	print('populating instructors...')
	populate_instructors()
	print('instructor population done...')

