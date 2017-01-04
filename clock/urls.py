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
    url(r'^profile/$', views.Profile, name="profile"),
    url(r'^employee_profile/$', views.Profile, name="employee_profile"),
    url(r'^employer_profile/$', views.Profile, name="employer_profile"),
    url(r'^logout/$', views.LogoutRequest, name="logout"),
    url(r'^employer_profile/employee_info/$', views.EmployeeInfo, name="employee_info"),
]