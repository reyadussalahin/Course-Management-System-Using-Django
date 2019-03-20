from django.db import models
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator

# from registration.models import User
from django.contrib.auth.models import User
from . import restrictions

class Course(models.Model):
	# remember django by default creates an primary key field named 'id'
	# it's add the following line in the model 
	# ''''''''id = models.AutoField(primary_key=True)'''''''
	# i can use this key to access Course object later where course is used as a foreignkey
	# for more details see views.py file...speacially views.course_list()
	# u'll get it
	creator = models.ForeignKey(User, null=False)
	student_key = models.CharField(max_length=restrictions.COURSE_KEY_LEN, null=False, unique=True)
	instructor_key = models.CharField(max_length=restrictions.COURSE_KEY_LEN, null=False, unique=True)
	course_name = models.CharField(max_length=restrictions.COURSE_NAME_LEN, blank=False, null=False)
	session_name = models.CharField(max_length=restrictions.COURSE_SESSION_NAME_LEN, blank=True, null=True)
	start_date = models.DateField(blank=True, null=True)
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '{}({})'.format(self.course_name, self.session_name)

	class Meta:
		unique_together = (('creator', 'course_name', 'session_name'), )



class Student(models.Model):
	# remember django by default creates an primary key field named 'id'
	# it's add the following line in the model 
	# ''''''''id = models.AutoField(primary_key=True)'''''''
	# i can use this key to access Student object later where student is used as a foreignkey
	# for more details see views.py file...speacially views.course_list()
	# u'll get it
	course = models.ForeignKey(Course, null=False)
	student = models.ForeignKey(User, null=False)
	# class_id = models.CharField(restrictions.STUDENT_ID_LEN)
	class_id = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(1)])
	is_deleted = models.BooleanField(default=False)
	added_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '{}({}) of {}({}) by {}'.format(
			self.student.username,
			self.class_id,
			self.course.course_name,
			self.course.session_name,
			self.course.creator)

	class Meta:
		unique_together = (('course', 'student'), ('course', 'class_id'), )




class Instructor(models.Model):
	course = models.ForeignKey(Course, null=False)
	instructor = models.ForeignKey(User, null=False)
	is_deleted = models.BooleanField(default=False)
	added_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '{} of {}({}) by {}'.format(
			self.instructor.username,
			self.course.course_name,
			self.course.session_name,
			self.course.creator)

	class Meta:
		unique_together = (('course', 'instructor'), )

	