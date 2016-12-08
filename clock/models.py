"""
models.py

@author Jason McMullen
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import RegexValidator
from clock.location_choices import *
from datetime import datetime, timedelta, time, date


# An extension of the BaseUser class    
class Employee(models.Model):

    numeric = RegexValidator(r'^[0-9]*$', 'Only numeric characters are allowed.')
    alpha = RegexValidator(r'^[A-za-z]*$', 'Only alpha characters are allowed.')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, null=False, blank=True, validators=[alpha])
    last_name = models.CharField(max_length=20, null=False, blank=True, validators=[alpha])
    phone = models.CharField(max_length=10, null=False, blank=True, validators=[numeric])
    pay_rate = models.FloatField(default=0.00, null=False, blank=True)
    
    def getAllPunches(self):
        all_punches = Punch.objects.filter(employee=self).order_by("-date")
        return all_punches
        
    def getTodaysPunches(self):
        todays_punches = Punch.objects.filter(employee=self, date=datetime.now()).order_by("-date")
        return todays_punches
        
    def getThisWeeksPunches(self):
        this_weeks_punches = Punch.objects.filter(employee=self, date__range=[datetime.now() - timedelta(days=7), datetime.now()]).order_by("-date")
        return this_weeks_punches
        
    def numOfPunches(self):
        total = Punch.objects.filter(employee=self).count()
        return total

    def isEvenNumPunches(self):
        total = Punch.objects.filter(employee=self).count()
        result = False
        if total == 0:
            result = True
        elif total % 2 == 0:
            result = True
        else:
            result = False
        return result
    
    """
    This will be calculated by finding the total number of seconds the employee has worked and
    then converting it to hours in decimal form
    """
    def hoursWorkedToday(self):
        punches = list(Punch.objects.filter(employee=self, date=datetime.now()).order_by("-date"))
        total = Punch.objects.filter(employee=self, date=datetime.now()).count()
        
        # Need the last check to stop an index out of bounds error when there are no punches
        # for that day.
        if total % 3 == 0 and total != 0:
            del punches[-1]

        start = None
        end = None
        total_seconds = 0.0
        
        for p in punches:
            if start == None:
                start = p.time
            else:
                end = p.time
                total_seconds += abs(end.hour - start.hour) * 3600
                total_seconds += abs(end.minute - start.minute) * 60
                total_seconds += abs(end.second - start.second)
                start = None
            
        return "%.2f" % (total_seconds / 3600)
        
    def hoursWorkedThisWeek(self):
        punches = list(Punch.objects.filter(employee=self, date__range=[datetime.now() - timedelta(days=7), datetime.now()]).order_by("-date"))
        total = len(punches)
        
        # Need the last check to stop an index out of bounds error when there are no punches
        # for that day.
        if total % 3 == 0 and total != 0:
            del punches[-1]

        start = None
        end = None
        total_seconds = 0.0
        
        for p in punches:
            if start == None:
                start = p.time
            else:
                end = p.time
                total_seconds += abs(end.hour - start.hour) * 3600
                total_seconds += abs(end.minute - start.minute) * 60
                total_seconds += abs(end.second - start.second)
                start = None
            
        return "%.2f" % (total_seconds / 3600)
    
    def __str__(self):
        return self.first_name + " " + self.last_name
        
# An extension of the BaseUser class
class Employer(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, null=False, blank=True)
    last_name = models.CharField(max_length=20, null=False, blank=True)
    
    def getAllEmployees(self):
        all_employees = Employee.objects.all()
        return all_employees
    
    def __str__(self):
        return "Name: " + self.first_name + " " + self.last_name

# Logic to handle all punch ins/outs. For now, accept all punch requests
class Punch(models.Model):

    employee = models.ForeignKey('Employee')
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(
        max_length=50,
        choices=LOCATION_CHOICES,
        default = OFFICE,
    )
    
    def __str__(self):

        # Format for time
        formatT = '%I:%M%p'

        # "American" date format
        formatD = "%a %b %d %Y"

        return self.date.strftime(formatD) + " " + self.time.strftime(formatT) + " " + self.location