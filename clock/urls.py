"""
urls.py

@author Jason McMullen
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Home, name="home"),
	url(r'^register/$', views.Register, name="register"),
	url(r'^login/$', views.LoginRequest, name="login"),
    url(r'^employee_profile/$', views.Profile, name="employee_profile"),
    url(r'^employer_profile/$', views.Profile, name="employer_profile"),
    url(r'^logout/$', views.LogoutRequest, name="logout"),
    url(r'^employee_profile/punch/$', views.PunchRequest, name="punch"),
]