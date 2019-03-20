from django.contrib import admin

# Register your models here.

from course.models import Course
from course.models import Student


admin.site.register(Course)
admin.site.register(Student)
