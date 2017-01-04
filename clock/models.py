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


"""
@ All information for the Employee class. Will also hold all methods needed to retrieve punches
@ related to an employee object.
"""  
class Employee(models.Model):

    numeric = RegexValidator(r'^[0-9]*$', 'Only numeric characters are allowed.')
    alpha = RegexValidator(r'^[A-za-z]*$', 'Only alpha characters are allowed.')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, null=False, blank=True, validators=[alpha])
    last_name = models.CharField(max_length=20, null=False, blank=True, validators=[alpha])
    phone = models.CharField(max_length=10, null=False, blank=True, validators=[numeric])
    pay_rate = models.FloatField(default=0.00, null=False, blank=True)
    
    """
    @ Method to return all punches for this employee
    @
    @return all of the punches for this employee
    """
    def getAllPunches(self):
        all_punches = Punch.objects.filter(employee=self).order_by("-date")
        return all_punches
    
    """
    @ Method to return all punches created today for this employee
    @
    @return all of todays punches for this employee
    """
    def getTodaysPunches(self):
        todays_punches = Punch.objects.filter(employee=self, date=datetime.now()).order_by("-date")
        return todays_punches
    
    """
    @ Method to return all punches created this week for this employee
    @
    @return all punches from this week for this employee
    """
    def getThisWeeksPunches(self):
        this_weeks_punches = Punch.objects.filter(employee=self, date__range=[datetime.now() - timedelta(days=7),
                                                  datetime.now()]).order_by("-date")
        return this_weeks_punches
       
    """
    @ Method to create the total number of punches for this employee
    @
    @return the total number of punches for this employee
    """
    def numOfPunches(self):
        total = Punch.objects.filter(employee=self).count()
        return total

    """
    @ Method that returns True if there is an even number of punches created for this employee, False otherwise.
    @
    @return True if an even number of punches has been created for this employee, False otherwise
    """
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
    @ This will be calculated by finding the total number of seconds the employee has worked and
    @ then converting it to hours in decimal form.
    @
    @return the total number of hours this employee has worked today
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
        
        # Since punches are in pairs, an out with every in, we need a way to record everyother punch
        # as an in. Same is true for outs, hence the need for the conditional below.
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
    
    """
    @Method that will calculate the total number of hours an employee has worked for this week.
    @
    @return the total number of hours this employee has worked this week
    """
    def hoursWorkedThisWeek(self):
        punches = list(Punch.objects.filter(employee=self, date__range=[datetime.now() - timedelta(days=7), 
                                            datetime.now()]).order_by("-date"))
        total = len(punches)

        # Need the last check to stop an index out of bounds error when there are no punches
        # for that day.
        if total % 3 == 0 and total != 0:
            del punches[-1]

        start = None
        end = None
        start_date = None
        end_date = None
        total_seconds = 0.0
        
        for p in punches:
            if start == None:
                start = p.time
                start_date = p.date
            else:
                end = p.time
                end_date = p.date
                total_seconds += abs(end.hour - start.hour) * 3600
                total_seconds += abs(end.minute - start.minute) * 60
                total_seconds += abs(end.second - start.second)
                total_seconds += abs(end_date - start_date).days * 86400
                start = None
            
        return "%.2f" % (total_seconds / 3600)
    
    """
    @ String representation of an instance of this class
    @
    @return a string representation of an employee
    """
    def __str__(self):
        return self.first_name + " " + self.last_name
        
"""
@ All information for an employer. This class will also contain methods that will retrieve employee 
@ information for the employer.
"""
class Employer(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, null=False, blank=True)
    last_name = models.CharField(max_length=20, null=False, blank=True)
    
    """
    @ Method to return all employee objects from the DB
    @
    @return a QuerySet containing all employee instances
    """
    def getAllEmployees(self):
        all_employees = Employee.objects.all()
        return all_employees
    
    """
    @ Method that creates a string representation of an employer
    @
    @return a string representation of an employer
    """
    def __str__(self):
        return "Name: " + self.first_name + " " + self.last_name

"""
@ Contains all information and logic for an employee to punch in an out of the system.
"""
class Punch(models.Model):

    employee = models.ForeignKey('Employee')
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(
        max_length=50,
        choices=LOCATION_CHOICES, # Choices is located in /location_choices.py
        default = OFFICE,
    )
   
    """
    @ Method that creates a string representation of a punch.
    @
    @return a string representation of a punch.
    """
    def __str__(self):

        # Format for time
        formatT = '%I:%M%p'

        # "American" date format
        formatD = "%a %b %d %Y"

        return self.date.strftime(formatD) + " " + self.time.strftime(formatT) + " " + self.location