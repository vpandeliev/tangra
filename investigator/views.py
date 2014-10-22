from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from studies.models import *
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
	return render_to_response('investigator/dashboard.html', locals(), context_instance=RequestContext(request))
