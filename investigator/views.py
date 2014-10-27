from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from studies.models import *
#from django.contrib.auth.models import User
from custom_auth.models import User
from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
	return dictionary.get(key)



def is_investigator(user, study):
	"""	Return True if the specified 'user' is an investigator for this 'study'. """
	if len(Study.objects.filter(id=study.id, investigators__id=user.id)) > 0:
		return True
	return False



@login_required
def show_study(request, study_id):
	"""	Display the study with 'study_id'. """
	study = Study.objects.get(id=study_id)

	if not is_investigator(request.user, study):
		# The user is not allowed to view this content
		# Redirect back to the list of active studies
		return HttpResponseRedirect(reverse('studies:active_studies'))

	# TODO: display the investigator view for a study
	groups = Group.objects.filter(study=study)

	stage_names = {}
	progress = {}
	for group in groups:
		# total number of stages group needs to complete
		total = (float) (GroupStage.objects.filter(group=group).count())
		for p in group.users.all():
			# get the stage names
			stages = UserStage.get_active_stages(p, study)
			try:
				stage_names[p.id] = stages[0].group_stage.stage.name
			except:
				stage_names[p.id] = None
			# calculate the progress
			completed = UserStage.objects.filter(user=p, group_stage__group=group, status=0).count()
			progress[p.id] = (int) ((completed / total) * 100)
	return render_to_response('investigator/overview.html', locals(), context_instance=RequestContext(request))



@login_required
def user_profile(request, study_id, user_id):
	""" Redirect to the user's first stage. """
	study = Study.objects.get(id=study_id)

	if not is_investigator(request.user, study):
		# The user is not allowed to view this content
		# Redirect back to the list of active studies
		return HttpResponseRedirect(reverse('studies:active_studies'))

	# Get the user stages for this user and study
	user_stages = UserStage.objects.filter(group_stage__stage__study__id=study_id, user__id=user_id).order_by("group_stage__order")

	# Redirect back to the overview page if they are not part of the study
	if user_stages is None:
		return HttpResponseRedirect(reverse('studies:investigator:show_study', args=[study_id]))

	# Redirect to the available stage
	# TODO: Find first active stage that a user is currently doing
	stage_number = user_stages[0].group_stage.order

	return HttpResponseRedirect(reverse('studies:investigator:user_stage', args=[study_id, user_id, stage_number]))



@login_required
def user_stage(request, study_id, user_id, stage_number):
	study = Study.objects.get(id=study_id)

	if not is_investigator(request.user, study):
		# The user is not allowed to view this content
		# Redirect back to the list of active studies
		return HttpResponseRedirect(reverse('studies:active_studies'))

	participant = User.objects.get(id=user_id)
	gender_choices = {0: 'Female', 1: 'Male', 2: 'Other'}
	user_stage = UserStage.objects.get(user=participant, group_stage__order=stage_number, group_stage__stage__study=study)
	data = Data.objects.filter(user_stage=user_stage).order_by("timestamp")
	stages = UserStage.objects.filter(user=participant, group_stage__stage__study=study).order_by("group_stage__order")
	hide_title=True

	return render_to_response('investigator/data.html', locals(), context_instance=RequestContext(request))
