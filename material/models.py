import os
import random
from datetime import datetime

from django.db import models
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator

from django.contrib.auth.models import User
from course.models import Course
from . import restrictions


class Topic(models.Model):
	# remember django by default creates an primary key field named 'id'
	# it's add the following line in the model 
	# ''''''''id = models.AutoField(primary_key=True)'''''''
	# i can use this key to access Topic object later where topic is used as a foreignkey
	creator = models.ForeignKey(User, null=False, related_name='topic_creator')
	updater = models.ForeignKey(User, null=False, related_name='topic_updater')
	course = models.ForeignKey(Course, null=False)
	topic_name = models.CharField(
		max_length=restrictions.TOPIC_NAME_LEN,
		blank=False,
		null=False)
	topic_description = models.TextField(blank=True, null=True)
	topic_serial = models.IntegerField(validators=[MinValueValidator(1)], null=False, blank=True)
	is_deleted = models.BooleanField(default=False)
	added_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '{}. {} of {}({})'.format(
			self.topic_serial,
			self.topic_name,
			self.course.course_name,
			self.course.session_name)

	class Meta:
		unique_together = (('course', 'topic_name'), ('course', 'topic_serial'), )



# new_file_name -> m{user_id}_{material_name_provided_by_instructor}
# you may use this format to extract material_name
# or you may just use the file name described in 'instance.material_name'
# it's completely ok....
# be aware when you're uploading file through population script
# it may not work as expected...because file name changes in those type of upload
# i don't know why
# this is done beacuse 'new file name' is needed for 'unique' 'file name' of our own choice
# to save in the material directory, as all the files are going there
def upload_path(instance, filename):
	if instance.material:
		fileid = instance.topic.id
		filename = instance.material_name
	else:
		random.seed(datetime.now())
		fileid = random.randint(int(1e9), int(1e10))
	new_filename = 'm{0}_{1}'.format(fileid, filename)
	path = 'materials'
	return os.path.join(path, new_filename)
	# so path becomes (an example): 'materials/m12introduction.pdf' inside media directory
	# where '12' is the material 'id' and 'introduction.pdf' is the filename
	# when no picture uploaded...we have to handle it securely


class Material(models.Model):
	creator = models.ForeignKey(User, null=False, related_name='material_creator')
	updater = models.ForeignKey(User, null=False, related_name='material_updater')
	topic = models.ForeignKey(Topic, null=False, related_name='material_topic')
	material = models.FileField(upload_to=upload_path, blank=False)
	material_name = models.CharField(
		blank=False,
		null=False,
		max_length=restrictions.MATERIAL_NAME_LEN)
	material_description = models.TextField(blank=True, null=True)
	material_serial = models.IntegerField(validators=[MinValueValidator(1)], null=False, blank=True)
	is_deleted = models.BooleanField(default=False)
	added_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '{} of {}'.format(
			self.material_name,
			self.topic.topic_name)

	class Meta:
		unique_together = (('topic', 'material_name'), ('topic', 'material_serial'), )

