from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from django.core.urlresolvers import reverse


# Templates used
TEMPLATE_LOGIN = "registration/login.html"

# Error messages for logging in
ERROR_INVALID_CREDENTIALS = "Sorry, that is not a valid username or password."
ERROR_DISABLED_ACCOUNT = "This account has been disabled."


class Values(object):
	"""	Attributes will be defined outside.
	http://stackoverflow.com/questions/1901525/django-template-and-the-locals-trick """
	pass



def home(request):
	"""	View displayed on the homepage. """
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))
	else:
		return HttpResponseRedirect(reverse('studies:active_studies'))



def login(request):
	"""	Log the requested user into Tangra """
	if request.method == 'GET':
		if request.user.is_authenticated():
			# User is already logged in
			return HttpResponseRedirect(reverse('home'))
		else:
			return render_to_response(TEMPLATE_LOGIN, {}, context_instance=RequestContext(request))

	elif request.method == 'POST':
		# TODO: Error if request doesn't have these parameters
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = auth.authenticate(username=username, password=password)

		if user is None:
			# Invalid credentials
			val = Values()
			val.errors = True
			val.message = ERROR_INVALID_CREDENTIALS
			return render_to_response(TEMPLATE_LOGIN, val.__dict__, context_instance=RequestContext(request))

		elif not user.is_active:
			# This user account has been disabled
			val = Values()
			val.errors = True
			val.message = ERROR_DISABLED_ACCOUNT
			return render_to_response(TEMPLATE_LOGIN, val.__dict__, context_instance=RequestContext(request))

		else:
			# User successfully logged in
			auth.login(request, user)
			return HttpResponseRedirect(reverse('home'))

	else:
		# Bad request: Only GET and POST methods are allowed
		return HttpResponseNotAllowed(['GET', 'POST'])



def logout(request):
	"""	Log the currently logged in user out of Tangra """
	auth.logout(request)
 	return HttpResponseRedirect(reverse('home'))
