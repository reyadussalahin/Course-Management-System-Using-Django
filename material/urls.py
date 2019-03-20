from django.conf.urls import url
from material import views

urlpatterns = [
    url(r'^topic/(?P<course_id>[\d]+)/', views.topic_list, name='topic_list'),
    url(r'^topic/add/(?P<course_id>[\d]+)/', views.add_topic, name='add_topic'),
    url(r'^material/(?P<topic_id>[\d]+)/', views.material_list, name='material_list'),
    url(r'^material/add/(?P<topic_id>[\d]+)/', views.add_material, name='add_material'),
    # url(r'^instructor/(?P<course_id>[\d]+)/', views.instructor_list, name='instructor_list'),
    # url(r'^logout/', views.logout, name='logout'),
    # url(r'^profile/(?P<username>[\w\-\.]+)/', views.profile, name='profile'),
]
