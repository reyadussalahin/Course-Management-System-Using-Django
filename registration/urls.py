from django.conf.urls import url
from registration import views

urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^profile/(?P<username>[\w\-\.]+)/', views.profile, name='profile'),
]
