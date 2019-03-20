from django.conf.urls import url
from course import views

urlpatterns = [
	url(r'^list/(?P<username>[\w\-\.]+)/', views.course_list, name='course_list'),
    url(r'^create/', views.create_course, name='create_course'),
    url(r'^instruct/', views.instruct_course, name='instruct_course'),
    url(r'^enroll/', views.enroll_course, name='enroll_course'),
    url(r'^index/(?P<course_id>[\d]+)/', views.course_index, name='course_index'),
    url(r'^student/(?P<course_id>[\d]+)/', views.student_list, name='student_list'),
    url(r'^instructor/(?P<course_id>[\d]+)/', views.instructor_list, name='instructor_list'),
    # url(r'^logout/', views.logout, name='logout'),
    # url(r'^profile/(?P<username>[\w\-\.]+)/', views.profile, name='profile'),
]
