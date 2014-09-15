from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from models import *

@login_required
def show_many_studies(request):
	# Get all of the stages are active
	current_stages = UserStage.objects.filter(user=request.user, status=1)
	return render_to_response('study/show_many_studies.html', locals(), context_instance=RequestContext(request))

@login_required
def show_one_study(request, s_id):
	study_id = int(s_id)
	request.session['study_id'] = study_id
	study = Study.objects.get(id=study_id)
	username = request.user.username

	stages = UserStage.objects.filter(user=request.user)
	current_stage = get_current_stage(study, request.user)

	if current_stage:
		action = current_stage.group_stage.stage.url
		return render_to_response('study/show_one_study.html', locals(), context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect(reverse('studies:show_many_studies'))