from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import timezone
from models import *
import json

@login_required
def show_active_studies(request):
	"""	Display all active stages that the user currently has. """
	
	# Assumes that there is one active stage per study
	# (Otherwise it would display duplicate studies in the list)
	
	# Getting stages from the user.
	current_stages = UserStage.get_active_stages(request.user)
	
	# Generating other local variable.
	investigator_studies = Study.objects.filter(investigators=request.user)	
	groups = {}
	for study in investigator_studies:
		groups[study.id] = Group.objects.filter(study=study)

	return render_to_response('study/show_active_studies.html', locals(), context_instance=RequestContext(request))

@login_required
def show_study(request, study_id):
	"""	Display the study with id 'study_id'. """
	
	request.session['study_id'] = study_id
	study = Study.objects.get(id=study_id)

	active_stages = UserStage.get_active_stages(request.user, study)

	if len(active_stages) <= 0:
		# There are no available actions to do within this study
		return HttpResponseRedirect(reverse('studies:active_studies'))

	stage = active_stages[0]

	return HttpResponseRedirect(reverse('studies:stage', args=[study_id, stage.group_stage.order]))

@login_required
def show_stage(request, study_id, stage_number):
	""" Display the stage_number'th stage of study with ID 's_id', for the
		participant who sent the request. """
	
	request.session['study_id'] = study_id
	study = Study.objects.get(id=study_id)

	if len(UserStage.get_active_stages(request.user, study)) <= 0:
		# There are no available actions to do within this study
		return HttpResponseRedirect(reverse('studies:active_studies'))

	# Get all of the user stages associated with this study (in order)
	stages = UserStage.objects.filter(user=request.user, group_stage__stage__study=study)
	stages = stages.order_by('group_stage__order')

	# Get the current stage to show information
	try:
		cur_stage = UserStage.objects.get(
			user=request.user,
			group_stage__stage__study=study,
			group_stage__order=stage_number)
	except:
		return HttpResponseRedirect(reverse('studies:active_studies'))

	return render_to_response('study/show_stage.html', locals(), context_instance=RequestContext(request))

@login_required
def render_stage(request, study_api_name, stage_url):
	""" Render the stage on a stage template. """
	
	# Hack Barrier. If anyone tries to access the study improperly, errors ensue!
	try:
		study = Study.objects.get(api_name=study_api_name)
		stage = Stage.objects.get(url=stage_url, study=study)
		user_stage = UserStage.objects.get(group_stage__stage__study=study, 
			                           user=request.user, status=1, 
			                           group_stage__stage=stage)
	except:
		return HttpResponseRedirect(reverse('studies:active_studies'))
	token = ""
	
	# Baking the token to be used.
	# TODO: Replace this with Session Authentication system.
	from rest_framework.authtoken.models import Token
	
					
	c = Token.objects.filter(user=request.user).count()
			
	# In this portal, a new token is made if a user has no token.
			
	if c > 0:
		token = str(Token.objects.get(user=request.user))
	else:
		token = str(Token.objects.create(user=request.user))
		
	# Setting up time variables.
	if user_stage.start_date == None:
		user_stage.start_date = timezone.now()
		user_stage.save()
		
	min_duration_over = user_stage.min_duration_over()
	wait_duration = user_stage.get_wait_duration()
	wait_duration_millisecond = wait_duration.total_seconds() * 1000;
	wait_until = user_stage.get_wait_until()
	
	# Redirect if the stage is unavailable.
	if not user_stage.is_available():
		return HttpResponseRedirect(reverse('studies:active_studies'))
	
	return render_to_response('studies/' + study_api_name + '/' + \
	                          stage_url + '.html', 
	                          locals(), 
	                          context_instance=RequestContext(request))

@login_required
def submit_stage(request, study_api_name, stage_url):
	""" Submit the result into the database.
	"""
	
	study = Study.objects.get(api_name=study_api_name)
	us = UserStage.objects.get(group_stage__stage__study=study, user=request.user, status=1)
	
	if request.method == 'POST':
		clean_dict = {}
		
		for k in request.POST:
			if k != 'csrfmiddlewaretoken':
				clean_dict[k] = request.POST[k]
				
		if len(clean_dict) > 0: # This condition cull blank data.
			new_data = Data.objects.create(user=request.user,
	                               timestamp=str(timezone.now()),
	                               user_stage=us,
	                               datum=json.dumps(clean_dict))
		
	
		us.complete_stage()
		next_us = get_next_user_stage(request.user, study)
		
		if next_us != None:
			next_us.start_stage()

	#return HttpResponseRedirect(reverse('studies:active_studies'))
	
	return show_study(request, study.id)