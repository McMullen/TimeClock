"""
models.py

@author Jason McMullen
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# An extension of the User class    
class Employee(models.Model):

    # Validator to control what the user is entering into the fields
    alpha = RegexValidator(r'^[a-zA-Z]*$', 'Only alpha characters without spaces are allowed.')

    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=20, null=False, blank=False, validators=[alpha])
    last_name = models.CharField(max_length=20, null=False, blank=False, validators=[alpha])
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    pay_rate = models.FloatField(default=0.00, null=False, blank=True)
    can_see_hours = models.BooleanField(default=False, null=False, blank=True)
    
    def getAllPunches(self):
        all_punches = Punch.objects.filter(employee=self)
        return all_punches
    
    def __str__(self):
        return "Name: " + self.fist_name + " " + self.last_name

AUTH_USER_MODEL = 'clock.Employee'
AUTH_PROFILE_MODULE = 'clock.Employee'

# Logic to handle all punch ins/outs. For now, accept all punch requests
class Punch(models.Model):

    date = models.DateField()
    time = models.TimeField()
    employee = models.ForeignKey('Employee')

    def __str__(self):

        # Format for time
        formatT = "%H:%M:%S"

        # "American" date format
        formatD = "%a %b %d %Y"

        return "Punch at " + " " + self.date.strftime(formatD) + " " +self.time.strftime(formatT)