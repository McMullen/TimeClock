"""
forms.py

@author Jason McMullen
"""

from clock.models import *
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from datetime import datetime, timedelta, time, date
from clock.location_choices import *
from datetimewidget.widgets import DateTimeWidget


"""
@ Form for collecting the basic information for an employee during the registration
@ process.
"""
class RegistrationForm(forms.Form):

    username = forms.CharField(label='User Name')
    email = forms.EmailField(label='E-Mail Address')
    password = forms.CharField(label='Password', widget=forms.PasswordInput(render_value=False))
    password1 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(render_value=False))
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    phone = forms.CharField(label='Phone Number')
    
    """
    @ Pull in all information from Employee class except for username
    """
    class Meta:
    
        model = Employee
        exclude = ('user',)
		
    """
	@ This method checks to see if the username is available for use
    """
    def clean_username(self):
    
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("That user name already exists. Please select another.")

    """
    @ This method checks to see if the passwords equal each other
    """
    def clean_password1(self):
        
        if self.cleaned_data.get('password') != self.cleaned_data.get('password1'):
            raise forms.ValidationError("The passwords did not match. Please try again.")
        return self.cleaned_data

"""
@ Information needed to be gathered for LoginRequest
"""
class LoginForm(forms.Form):

    username = forms.CharField(label='User Name')
    password = forms.CharField(label='Password', widget=forms.PasswordInput(render_value=False))

"""
@ Employee punch in form
@
@ This form will ask the employee for the location that they will begin working at
"""
class PunchInForm(forms.Form):

    location = forms.ChoiceField(widget=forms.RadioSelect(), choices=LOCATION_CHOICES, required = True,)
    
"""
@ Employee punch out form
@
@ This form will NOT ask the employee for their location and instead will record an Out
"""
class PunchOutForm(forms.Form):

    location = "Out"
    
"""
@ Form for selecting an employee and viewing information about them
"""
class EmployeeInfoForm(forms.Form):

    class Meta:
        model = Employee
        widgets = {
            'datetime': DateTimeWidget()
        }

    dateTimeOptions = {
       'format': 'mm/dd/yyyy',
        'autoclose': 'true',
        'todayBtn': 'true',
        'todayHighlight': 'true',
        'minView': '2',
        'maxView': '2', 
    }
        
    start_date = forms.DateField(widget=DateTimeWidget(options = dateTimeOptions))
    end_date = forms.DateField(widget=DateTimeWidget(options = dateTimeOptions))
    