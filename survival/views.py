from django.shortcuts import render
from django.http import HttpResponse
from . import survival
import json
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth
from models import subscribeList

from mailchimp import utils
MAILCHIMP_LIST_ID = 'ea2be558d7' # KM Survival Newsletter


def home(request):
	return render(request, 'survival/home.html')

def survey(request):
	return render(request, 'survival/survey.html')

def random_curve(request):
	return render(request, 'survival/random_curve.html')

def random_data(request):
	data = survival.random_data()
	return HttpResponse(data, content_type="application/json")

def input_data(request):
	return render(request, 'survival/input_data.html')

def humza_input(request):
	return render(request, 'survival/humza_input.html')

def about(request):
	return render(request, 'survival/about.html')

def generate_curve(request):
	
	if request.method == 'POST':
		data = json.loads(request.body)
		data = survival.generate_curve(data)
		return HttpResponse(data, content_type="application/json")
	else:
		return HttpResponse(
            json.dumps({"nothing to see": "here"}),
            content_type="application/json"
        )


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("home.html")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = auth.authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                auth.login(request, user)
                return HttpResponseRedirect('login')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('registration/login.html', {}, context)

def user_logout(request):
	return render(request, 'survival/humza_input.html')

def subscribe(request):

	context = RequestContext(request)

	if request.method == 'POST':
		name = request.POST['personalName']
		email = request.POST['emailAddress']
		list = utils.get_connection().get_list_by_id(MAILCHIMP_LIST_ID)
        list.subscribe(email_address, {'EMAIL': email_address, 'FNAME': name})
		return HttpResponse("Subscribed Successfully!")
	else:
		return HttpResponse("Error. Unable to subscribe.")
