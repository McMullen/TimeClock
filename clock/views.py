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

            # Save all of the gathered information into a patient object
            patient = Patient(user=user,
                              first_name=form.cleaned_data['first_name'],
                              mid_initial=form.cleaned_data['mid_initial'],
                              last_name=form.cleaned_data['last_name'],
                              phone=form.cleaned_data['phone'],
                             )

            patient.save()

            # Auto sign in user
            patient = authenticate(username=form.cleaned_data['username'],
                                   password=form.cleaned_data['password'])
            login(request, patient)

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

                # log login activity if not superuser
                if not user.is_superuser:
                    newLog = ActivityLog(user=request.user.username,time_logged=datetime.now(),message=request.user.username + ' logged in')
                    newLog.save()
                return HttpResponseRedirect('/profile/')
            else:
                return render_to_response('login.html', {'form': form }, context_instance=RequestContext(request))

        # Something wrong with the form, send them back to make corrections
        else:
            return render_to_response('login.html', {'form': form }, context_instance=RequestContext(request))
    else:
        form = LoginForm()
        context = {'form': form}
        return render(request, 'login.html', context)
