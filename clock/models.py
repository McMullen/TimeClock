"""
models.py

@author Jason McMullen
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ObjectDoesNotExist

# An extension of the User class
class BaseUser(models.Model):
    # Validator to control what the user is entering into the fields
    alpha = RegexValidator(r'^[a-zA-Z]*$', 'Only alpha characters without spaces are allowed.')
    
    user = models.OneToOneField(User)
    username = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20, null=False, blank=False, validators=[alpha])
    last_name = models.CharField(max_length=20, null=False, blank=False, validators=[alpha])
    phone = models.CharField(max_length=20, null=False, blank=False)
    
    def is_employee(self):
        try:
            self.employee
        except Employee.DoesNotExist:
            return False
        else:
            return True
            
    def is_employer(self):
        try:
            self.employer
        except Employer.DoesNotExist:
            return False
        else:
            return True
    
# An extension of the BaseUser class    
class Employee(models.Model):

    user = models.OneToOneField(BaseUser)
    pay_rate = models.FloatField(default=0.00, null=False, blank=True)
    
    def getAllPunches(self):
        all_punches = Punch.objects.filter(employee=self)
        return all_punches
    
    def __str__(self):
        return "Name: " + self.fist_name + " " + self.last_name

# An extension of the BaseUser class
class Employer(models.Model):
    user = models.OneToOneField(BaseUser)
    
    def __str__(self):
        return "Name: " + self.first_name + " " + self.last_name

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