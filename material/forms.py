from django.utils.translation import gettext_lazy as _
from django import forms

from . import restrictions
from course_management import settings

from material.models import Topic
from material.models import Material


class TopicForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		self.course = kwargs.pop('course', None)
		super(TopicForm, self).__init__(*args, **kwargs)

	class Meta:
		model = Topic
		widgets = {
			'topic_description' : forms.Textarea(
					attrs = {
						'rows' : 8,
						'cols' : 16,
					}
				),
		}
		help_texts = {
			'topic_name' : _('Enter a topic name. Max 255 characters'),
			'topic_description' : _('Add a description for this topic'),
			'topic_serial' :
				_('In which no. do you want to appear this topic.\n'
					+ 'If kept empty or enter a value greater than present count of topics,\n'
					+ 'topic will be added at last'),
		}
		fields = ('topic_name', 'topic_description', 'topic_serial', )


	def clean_topic_name(self):
		topic_name = self.cleaned_data['topic_name']
		topic_name_len = len(topic_name)
		if topic_name_len > restrictions.TOPIC_NAME_LEN:
			raise forms.ValidationError(
					_('Name must be less than or equal to 255 characters'),
				)
		return topic_name

	def clean_topic_description(self):
		topic_description = self.cleaned_data['topic_description']
		return topic_description

	def clean_topic_serial(self):
		topic_serial = self.cleaned_data['topic_serial']
		if topic_serial and topic_serial < 1:
			raise forms.ValidationError(
					_('Enter a postive integer'),
				)
		return topic_serial

	def clean(self):
		cleaned_data = super(TopicForm, self).clean()
		topic_name = cleaned_data.get('topic_name', None)
		course = self.course
		if Topic.objects.filter(course=course, topic_name=topic_name).exists():
			raise forms.ValidationError(
					_('{} is already provided as a topic name in this course'.format(topic_name))
				)
		return cleaned_data




class MaterialForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		self.topic = kwargs.pop('topic', None)
		super(MaterialForm, self).__init__(*args, **kwargs)

	class Meta:
		model = Material
		widgets = {
			'material_description' : forms.Textarea(
					attrs = {
						'rows' : 8,
						'cols' : 16,
					}
				),
		}
		# labels = {
		# 	'material' : 'upload file',
		# }
		help_texts = {
			'material_name' : _('max 255 characters'),
		}
		fields = ('material_name', 'material_description', 'material', )

	def clean_material_name(self):
		material_name = self.cleaned_data['material_name']
		if len(material_name) > restrictions.MATERIAL_NAME_LEN:
			raise forms.ValidationError(
					_('max name length 255 chcracters'),
				)
		return material_name

	def clean_material_description(self):
		return self.cleaned_data['material_description']

	def clean(self):
		cleaned_data = super(MaterialForm, self).clean()
		material_name = cleaned_data.get('material_name', None)
		topic = self.topic
		if Material.objects.filter(topic=topic, material_name=material_name).exists():
			raise forms.ValidationError(
					_('A file is already named \'{}\'. Change the name'.format(material_name))
				)
		return cleaned_data

