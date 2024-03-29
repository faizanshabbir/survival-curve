from django.shortcuts import render
from django.http import HttpResponse
from . import survival
import json
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth
from models import subscribeList
from models import contactForm
from forms import ContactKMForm
from forms import basicUserSignup
from django.contrib.auth.models import Group, User
import stripe

from mailchimp import utils
MAILCHIMP_LIST_ID = 'ea2be558d7' # KM Survival Newsletter

from django.contrib.auth.decorators import user_passes_test

def group_required(request,*group_names):
    """Requires user membership in at least one of the groups passed in."""
    # def in_groups(request,group_names):
    if request.user.is_authenticated():
        groups_of_user = request.user.groups.values_list('name',flat=True)
        for group in group_names:
            if group in groups_of_user:
                return True
    return False
    # return in_groups(request,group_names)

def home(request):
	return render(request, 'survival/home_crafty.html', {'page_name': 'home'})

def contact(request):
    return render(request, 'survival/contact_crafty.html', {'page_name': 'contact'})

def home_telephasic(request):
	return render(request, 'survival/home_telephasic.html')

def survey(request):
	return render(request, 'survival/survey.html')

def about(request):
	return render(request, 'survival/about_crafty.html', {'page_name': 'about'})  

def sign_up(request):
    return render(request, 'survival/sign_up_crafty.html')

def email_signup(request):
    return render(request, 'survival/email_signup.html')

def random_data(request):
    data = survival.random_data()
    return HttpResponse(data, content_type="application/json")

def curve(request):
    return render(request, 'survival/curve.html', {'page_name': 'curve'})

def humza_input(request):
    return render(request, 'survival/humza_input.html')

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

def contactKM(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = ContactKMForm(request.POST)

        if form.is_valid():
            name = request.POST['name']
            email = request.POST['email']
            message = request.POST['message']

            ContactForm_obj = contactForm(name = name, email = email, message = message)
            ContactForm_obj = ContactForm_obj.save()

            return HttpResponse("Contact Message Sent!")
    else:
        return HttpResponse("Error. Unable to send contact message.")

def register(request):
    if request.method == 'POST':
        form = basicUserSignup(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password1']
            new_user = form.save()
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            #add user to basic user group
            return HttpResponseRedirect("survival/payment.html")
    else:
        form = basicUserSignup()
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

def subscribe(request):
    context = RequestContext(request)

    if request.method == 'POST':
        name = request.POST['personalName']
        email = request.POST['emailAddress']
        list = utils.get_connection().get_list_by_id(MAILCHIMP_LIST_ID)
        list.subscribe(email, {'EMAIL': email})
        return HttpResponse("Subscribed Successfully!")
    else:
        return HttpResponse("Error. Unable to subscribe.")

def payment(request):
    return render(request, "survival/payment.html")

def process_payment(request):
    # Set your secret key: remember to change this to your live secret key in production
    # See your keys here https://dashboard.stripe.com/account/apikeys
    stripe.api_key = "sk_test_7kmr2dA30d1UxmnVNMRoG4Wd"

    # Get the credit card details submitted by the form
    token = request.POST['stripeToken']

    # Create the charge on Stripe's servers - this will charge the user's card
    try:
        charge = stripe.Charge.create(
          amount=500, # amount in cents, again
          currency="usd",
          source=token,
          description="Example charge"
        )
        g = Group.objects.get(name = 'paid user')
        g.user_set.add(request.user)
        return HttpResponse("Successfully added to paid user group because of successful payment")
    except stripe.error.CardError, e:
        # The card has been declined
        return HttpResponse("Card didnt work")

def checkPerm(request):
    if group_required(request,'basic_user'):
        return HttpResponse('You are a basic user')
    elif group_required(request, 'paid_user'):
        return HttpResponse('You are a paid user')
    else:
        return HttpResponse('None of those worked')


def download(request):
	print "downloading"
	return HttpResponse("Hello")