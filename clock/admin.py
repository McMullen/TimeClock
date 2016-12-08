from django.contrib import admin
from .models import Employee, Employer, Punch

admin.site.register(Employee)
admin.site.register(Employer)
admin.site.register(Punch)