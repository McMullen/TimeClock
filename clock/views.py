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
from clock.forms import RegistrationForm, LoginForm
from clock.models import Employee, Punch

"""
Basic home page view
"""
def Home(request):
    return render_to_response("index.html")

"""
Register new users to the time clock system
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
                                                                       password=form.cleaned_data['password'])
            user.save()
            
            # Save all of the gathered information into a employee object
            employee = Employee(user=user,
                              first_name=form.cleaned_data['first_name'],
                              last_name=form.cleaned_data['last_name'],
                              phone_number=form.cleaned_data['phone'],
                              pay_rate=10.00,
                              can_see_hours=False,
                             )

            employee.save()

            # Auto sign in user
            employee = authenticate(username=form.cleaned_data['username'],
                                   password=form.cleaned_data['password'])
            login(request, employee)

            # Send the user to their profile page
            return HttpResponseRedirect('/profile/')
        else:
            # Send the form that is not valid back to register.html and display the errors to be fixed
            return render(request, 'register.html', {'form': form})

    else:
        # Send the form that is not valid back to register.html and display the errors to be fixed
        form = RegistrationForm()
        context = {'form' : form}
        return render(request, 'register.html', context)

"""
Handle login requests
"""
def LoginRequest(request):

    # Check if already logged in - if so send to profile instead of login page
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile/')

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

                return HttpResponseRedirect('/profile/')
            else:
                return render(request, 'login.html', {'form': form })

        # Something wrong with the form, send them back to make corrections
        else:
            context = {'form': form}
            return render(request, 'login.html', context)
    else:
        form = LoginForm()
        context = {'form': form}
        return render(request, 'login.html', context)

"""
Handle navigation to the profile page after successful login
"""
@login_required
def Profile(request):
    # If user is not logged in, send them to login page
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')

    user = User.objects.get(id=request.user.id)
    employee = Employee.objects.filter(user=user).get()
    context = {'employee': employee}
    return render(request, 'profile.html', context)