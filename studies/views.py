from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from models import *

@login_required
def show_active_studies(request):
	"""	Display all active stages that the user currently has. """
	# Assumes that there is one active stage per study
	# (Otherwise it would display duplicate studies in the list)
	# TODO: Instead use this to return a list of studies
	current_stages = UserStage.get_active_stages(request.user)
	investigator_studies = Study.objects.filter(investigators=request.user)
	return render_to_response('study/show_active_studies.html', locals(), context_instance=RequestContext(request))

@login_required
def show_study(request, s_id):
	"""	Display the study with id 's_id'. """
	study_id = int(s_id)
	request.session['study_id'] = study_id
	study = Study.objects.get(id=study_id)
	username = request.user.username

	# Get all of the user stages associated with this study (in order)
	stages = UserStage.objects.filter(user=request.user, group_stage__stage__study=study)
	stages = stages.order_by('group_stage__order')

	if len(UserStage.get_active_stages(request.user, study)) > 0:
		# There are active stages associated with this study
		return render_to_response('study/old_show_study.html', locals(), context_instance=RequestContext(request))
	else:
		# There are no available actions to do within this study
		return HttpResponseRedirect(reverse('studies:active_studies'))
