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
]