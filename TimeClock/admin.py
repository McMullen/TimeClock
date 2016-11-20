"""
admin.py

@author Jason McMullen
"""
from django.contrib.admin.sites import AdminSite
from django.contrib import admin
from clock.models import BaseUser, Employee, Employer

admin.site.register(BaseUser)
admin.site.register(Employee)
admin.site.register(Employer)