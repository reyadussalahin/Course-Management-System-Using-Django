from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django import forms

from registration.models import UserProfile
from . import restrictions



class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	confirm_password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		help_texts = {
			# _() is gettext_lazy method....see import
			# 'email' : _('Enter a valid email'),
			'password' : _('Password should be at least 8 characters long'),
		}
		labels = {
			'confirm_password' : _('Confirm Password'),
		}
		fields = ('first_name', 'last_name', 'username', 'email', 'password', )


	def clean_first_name(self): # does nothing
		return self.cleaned_data['first_name']


	def clean_last_name(self): # does nothing
		return self.cleaned_data['last_name']


	def clean_username(self): # it does nothing
		username = self.cleaned_data['username']
		return username


	def clean_email(self):
		email = self.cleaned_data['email']
		if len(email) == 0:
			raise forms.ValidationError(
					_('Please enter an valid email address'),
				)
		username = self.cleaned_data['username']
		if email and User.objects.filter(email=email).exclude(username=username).exists():
			raise forms.ValidationError(
					_('Email address already exists'),
				)
		return email


	def clean_password(self):
		password = self.cleaned_data['password']
		if len(password) < restrictions.MIN_PASSWORD_LEN:
			raise forms.ValidationError(
					_('Password should be at least 8 characters long'),
				)
		return password

	def clean(self):
		cleaned_data = super(UserForm, self).clean()
		password = cleaned_data['password']
		confirm_password = cleaned_data['confirm_password']

		# print('pw: {}'.format(password))
		# print('confirm_pw: {}'.format(confirm_password))
		
		if password != confirm_password:
			raise forms.ValidationError(
					_('Please confirm password correctly'),
				)
		return cleaned_data




class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('picture', )
