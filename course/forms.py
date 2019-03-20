from django.utils.translation import gettext_lazy as _
from django import forms

from course.models import Course
from course.models import Student
from course.models import Instructor
from . import restrictions
from course_management import settings

class CourseForm(forms.ModelForm):
	start_date = forms.DateField(
		help_text='use (dd-mm-yyyy)',
		widget=forms.DateInput(format='%d-%m-%Y'),
		input_formats=('%d-%m-%Y', ))

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(CourseForm, self).__init__(*args, **kwargs)


	class Meta:
		model = Course
		# widgets = {
		# 	'start_date' : forms.DateInput(format='%d-%m-%y'),
		# }
		help_texts = {
			'course_name' : _('max 255 characters'),
			# 'session_name' : _('max 255 characters'),
		}
		labels = {
			'session_name' : _('Session'),
		}
		fields = ('course_name', 'session_name', 'start_date', )

	def clean_course_name(self):
		course_name = self.cleaned_data['course_name']
		print('course_name: {}'.format(course_name))
		course_name_len = len(course_name)
		if course_name_len < 1 or course_name_len > restrictions.COURSE_NAME_LEN:
			raise forms.ValidationError(
					_('Enter course name properly'),
				)
		return course_name

	def clean_session_name(self):
		session_name = self.cleaned_data['session_name']
		return session_name

	def clean_start_date(self):
		start_date = self.cleaned_data['start_date']
		return start_date

	def clean(self):
		cleaned_data = super(CourseForm, self).clean()

		if settings.DEBUG:
			print('cleaned data: {}'.format(cleaned_data))
		
		course_name = cleaned_data.get('course_name', None)
		session_name = cleaned_data.get('session_name', None)
		creator = self.user
		if creator and Course.objects.filter(
			creator=creator,
			course_name=course_name,
			session_name=session_name).exists():
			raise forms.ValidationError(
					_('Course with this session name already exists.' +
						'Please create course with new name or provide a different session name')
				)
		return cleaned_data



class StudentForm(forms.ModelForm):
	student_key = forms.CharField(
		max_length=restrictions.COURSE_KEY_LEN,
		help_text='A secured key formed of 48 characters',
		label='Course Key(Student)')


	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(StudentForm, self).__init__(*args, **kwargs)

	class Meta:
		model = Student
		help_texts = {
			'class_id' : _('Enter the ID provided by the course creator to identify you uniquely in class'),
		}
		fields = ('class_id', )


	def clean_student_key(self):
		student_key = self.cleaned_data['student_key']
		if len(student_key) != restrictions.COURSE_KEY_LEN:
			raise forms.ValidationError(
					_('Enter a valid key'),
				)
		if not Course.objects.filter(student_key=student_key).exists():
			raise forms.ValidationError(
					_('No course exists with provided key'),
				)
		return student_key

	def clean_student_id(self):
		return self.cleaned_data['class_id']

	def clean(self):
		cleaned_data = super(StudentForm, self).clean()

		if settings.DEBUG:
			print('student reg data: {}'.format(cleaned_data))

		student_key = cleaned_data.get('student_key', None)
		class_id = cleaned_data.get('class_id', None)

		student = self.user
		try:
			course = Course.objects.get(student_key=student_key)
		except Course.DoesNotExist:
			raise forms.ValidationError(
					_('Course with provided key does not exist')
				)

		if Student.objects.filter(student=student, course=course).exists():
			raise ValidationError(
					_('You are already registered in this course'),
				)

		if Student.objects.filter(course=course, class_id=class_id).exists():
			raise ValidationError(
					_('Student ID already taken. Please enter a valid student id.'),
				)
		return cleaned_data



class InstructorForm(forms.ModelForm):
	instructor_key = forms.CharField(
		max_length=restrictions.COURSE_KEY_LEN,
		help_text='A secured key formed of 48 characters',
		label='Course Key(Instructor)')

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(InstructorForm, self).__init__(*args, **kwargs)

	class Meta:
		model = Instructor
		fields = tuple()


	def clean_instructor_key(self):
		instructor_key = self.cleaned_data['instructor_key']
		if len(instructor_key) != restrictions.COURSE_KEY_LEN:
			raise forms.ValidationError(
					_('Enter a valid key'),
				)
		if not Course.objects.filter(instructor_key=instructor_key).exists():
			raise forms.ValidationError(
					_('No course exists with provided key'),
				)
		return instructor_key


	def clean(self):
		cleaned_data = super(InstructorForm, self).clean()

		if settings.DEBUG:
			print(cleaned_data)

		instructor_key = cleaned_data.get('instructor_key', None)
		instructor = self.user
		try:
			course = Course.objects.get(instructor_key=instructor_key)
		except Course.DoesNotExist:
			raise forms.ValidationError(
					_('Course with provided key does not exist')
				)

		if Instructor.objects.filter(instructor=instructor, course=course).exists():
			raise ValidationError(
					_('You are already an instructor of this course'),
				)
		return cleaned_data
