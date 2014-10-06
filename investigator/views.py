from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from studies.models import *

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
	return HttpResponseRedirect(reverse('studies:active_studies'))