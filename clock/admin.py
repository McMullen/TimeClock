from django.contrib import admin
from .models import Employee, Employer, Punch

# Allow the superuser to add and modify these objects 
admin.site.register(Employee)
admin.site.register(Employer)
admin.site.register(Punch)