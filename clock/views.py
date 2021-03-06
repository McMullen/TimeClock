"""
views.py

@author Jason McMullen
"""

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from clock.forms import RegistrationForm, LoginForm, PunchInForm, PunchOutForm, EmployeeInfoForm
from clock.models import Employee, Employer, Punch
from datetime import datetime, time, date

"""
@ Basic home page view
"""
def Home(request):
    return render_to_response("index.html")

"""
@ Register new users to the time clock system
"""
def Register(request):
	
	# If already logged in, do not let the user reregister
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile/')
	
	# If the user submits a form
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        # Pass form back through all the clean methods we had created and make new user
        if form.is_valid():
            
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                                email = form.cleaned_data['email'],
                                                password=form.cleaned_data['password'],
                                                first_name=form.cleaned_data['first_name'],
                                                last_name=form.cleaned_data['last_name']
                                            )
            
            # Save all of the gathered information into a BaseUser object
            employee = Employee(user=user,
                                first_name = user.first_name,
                                last_name = user.last_name,
                                phone=form.cleaned_data['phone'],
                                pay_rate=10.00,
                               )

            user.save()
            employee.save()

            # Auto sign in user
            employee = authenticate(username=form.cleaned_data['username'],
                                   password=form.cleaned_data['password'])
            login(request, employee)

            # Send the user to their profile page
            return HttpResponseRedirect('/employee_profile/')
        else:
            # Send the form that is not valid back to register.html and display the errors to be fixed
            return render(request, 'register.html', {'form': form})

    else:
        # Send the form that is not valid back to register.html and display the errors to be fixed
        form = RegistrationForm()
        context = {'form' : form}
        return render(request, 'register.html', context)

"""
@ Handle login requests
"""
def LoginRequest(request):

    # Check if already logged in - if so send to profile instead of login page
    if request.user.is_authenticated():
        return HttpResponseRedirect('/employee_profile/')

    # If user is not logged in, gather information entered in login page
    if request.method == 'POST':

        form = LoginForm(request.POST)

        # If the form is valid, gather the information on the page and process it
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # This step is logging the user in
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                else:
                    return HttpResponseRedirect('/')

                return HttpResponseRedirect('/employee_profile/')
            else:
                return render(request, 'login.html', {'form': form})

        # Something wrong with the form, send them back to make corrections
        else:
            context = {'form': form}
            return render(request, 'login.html', context)
    else:
        form = LoginForm()
        context = {'form': form}
        return render(request, 'login.html', context)
        
"""
@ Handle logout requests
"""
def LogoutRequest(request):
    logout(request)
    return HttpResponseRedirect('/')

"""
@ Handle navigation to the profile page after successful login
"""
@login_required
def Profile(request):

    # If user is not logged in, send them to login page
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
        
    user = request.user
    
    # First try if the user is an employee; if so, send them to the employee profile page
    try:
        employee = user.employee
        
        # First time to the page, the browser will send a GET request. Since we want information
        # for the punch, we need to send a form to get a POST resquest back
        if request.method == 'POST':
            if employee.isEvenNumPunches():
                form = PunchInForm(request.POST)
                if form.is_valid():
                    location = form.cleaned_data['location']
                    ProfileHelper(location, employee)
            else:
                form = PunchOutForm(request.POST)
                if form.is_valid():
                    location = "Out"
                    ProfileHelper(location, employee)
            
            return HttpResponseRedirect('/employee_profile/')
        else:
            if employee.isEvenNumPunches():
                form = PunchInForm()		
                context = {'form': form, 'employee': employee}
                return render(request, 'employee_profile.html', context)
            else:
                form = PunchOutForm()		
                context = {'form': form, 'employee': employee}
                return render(request, 'employee_profile.html', context)

    
    # Second, try if user is an employer; if so, send them to the employer profile page
    except ObjectDoesNotExist:
        try:
            employer = user.employer
            
            if request.method == 'POST':
                form = EmployeeInfoForm(request.POST)
                if form.is_valid():
                    start = form.cleaned_data['start_date']
                    end = form.cleaned_data['end_date']
                    
                    for emp in employer.getAllEmployees():
                        emp.start_date = start
                        emp.end_date = end
                        emp.save()
                    
                context = {'employer' : employer, 'form': form}
                return render(request, 'employer_profile.html', context)
        
            else:
                form = EmployeeInfoForm()
                context = {'form': form, 'employer': employer}
                return render(request, 'employer_profile.html', context)
        
        # If the user is not an employee or an employer, then the user must be an admin
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/admin/')
            
"""
@ Helper method for Profile
@ param punch_location - the location the employee will be punching in/out from
@ param employee - the employee the punch will be saved to
"""
def ProfileHelper(punch_location, employee):
    date = datetime.now().date()
    time = datetime.now().time()
    location = punch_location
    punch = Punch(employee=employee,
                  date = date,
                  time = time,
                  location = location,
                 )
    punch.save()
            
