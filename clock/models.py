"""
models.py

@author Jason McMullen
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import RegexValidator

# An extension of the BaseUser class    
class Employee(models.Model):

    numeric = RegexValidator(r'^[0-9]*$', 'Only numeric characters are allowed.')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, null=False, blank=True, validators=[numeric])
    pay_rate = models.FloatField(default=0.00, null=False, blank=True)
    
    def getAllPunches(self):
        all_punches = Punch.objects.filter(employee=self)
        return all_punches
    
    def __str__(self):
        return "Name: " + self.fist_name + " " + self.last_name

# An extension of the BaseUser class
class Employer(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
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

        return self.date.strftime(formatD) + " " +self.time.strftime(formatT)