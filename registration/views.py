import os
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from registration.models import UserProfile
from registration.forms import UserForm
from registration.forms import UserProfileForm

from course_management import settings

# Create your views here.


def register(request):
	if request.method == 'POST':
		user_form = UserForm(request.POST, request.FILES)
		profile_form = UserProfileForm(request.POST, request.FILES)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save(commit=False)
			raw_password = user.password # this will be used in logging in user later...see below
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user
			profile.save()

			# logging in user after completing registration
			user = auth.authenticate(username=user.username, password=raw_password)
			auth.login(request, user)
			return HttpResponseRedirect(reverse('index'))
		else:
			print(user_form.errors)
			print(profile_form.errors)
			# it is happening for validation errors
			# and see we are not returning anything
			# may be django handles it itself
			# beacuse django retuns this form with telling error messages
			# if we show the validation error messages to user in the template
			# so that they may enter correct value
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	context = {
		'user_form' : user_form,
		'profile_form': profile_form,
	}

	return render(request, 'registration/register.html', context=context)



def login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = auth.authenticate(username=username, password=password)

		if user:
			if user.is_active:
				auth.login(request, user)
				return HttpResponseRedirect(reverse('index'))
			
			# i.e. user is not active....so we return the following message
			return HttpResponse('Your id is inactive i.e. disabled')

		# i.e. user can't login....cause invalid details
		return HttpResponse('Invalid login details provided')
	
	# i.e. method is get
	context = {}
	return render(request, 'registration/login.html', context=context)



def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(reverse('index'))



def process_profile_picture_name(name):
	# we are processing name to show the name as the profile picture name was in user os
	# to make file name different a processing has been done
	# to understand that go to models.py and read UserProfile class
	# there is a function for picture upload_to=upload_path does this change
	# i am going to use this process for file names in material app
	new_name = os.path.split(name)[1]
	return new_name.split('_', 1)[1]

def profile(request, username):
	# username = request.user.username
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		raise Http404("user not found")

	profile = UserProfile.objects.get(user=user)
	if profile.picture:
		# print('pic name: {}'.format(profile.picture.name))
		# print('pic path: {}'.format(profile.picture.path))
		# print('pic url: {}'.format(profile.picture.url))
		profile.picture.new_name = process_profile_picture_name(profile.picture.name)
		# print('pic name: {}'.format(profile.picture.name))
		# print('pic path: {}'.format(profile.picture.path))
		# print('pic url: {}'.format(profile.picture.url))

	context = {
		'profile' : profile
	}

	if settings.DEBUG:
		print('checking profile:')
		print('logged_in: {}'.format(request.user.username))
		print('profile_check: {}'.format(profile.user.username))

	return render(request, 'registration/profile.html', context=context)
