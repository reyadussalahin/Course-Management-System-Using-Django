import os
import random
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


# Create your models here.



# new_file_name -> p{user_id}_{file_name_in_user_os}
# use this format to extract file_name in user_os
# new_file_name is needed for unique file_name of our own choice
def upload_path(instance, filename):
	if instance.picture:
		fileid = instance.user.id
	else:
		random.seed(datetime.now())
		fileid = random.randint(int(1e9), int(1e10))
	new_filename = 'p{0}_{1}'.format(fileid, filename)
	path = 'profile_images'
	return os.path.join(path, new_filename)
	# no picture uploaded...we have to handle it securely



class UserProfile(models.Model):
	user = models.OneToOneField(User, unique=True)
	picture = models.ImageField(upload_to=upload_path, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	last_login = models.DateTimeField(blank=True, null=True)
	last_logout = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return self.user.username

