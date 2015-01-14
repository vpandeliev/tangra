from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse, StreamingHttpResponse
from django.core.urlresolvers import reverse
from studies.models import *
from studies.forms import *
from custom_auth.models import User
from django.template.defaulttags import register
from django.utils.encoding import smart_str
from itertools import chain
import csv
from django.core.mail import send_mail


@register.filter
def get_item(dictionary, key):
	""" Helper function that allows you to get items with a 'key' from a 'dictionary' 
		in the template view. """
	return dictionary.get(key)



def is_investigator(user, study):
	"""	Return True if the specified 'user' is an investigator for this 'study'. """
	if len(Study.objects.filter(id=study.id, investigators__id=user.id)) > 0:
		return True
	return False



@login_required
def show_study(request, study_id):
	"""	Display the study Dashboard with an ID 'study_id'. """
	study = Study.objects.get(id=study_id)

	if not is_investigator(request.user, study):
		# The user is not allowed to view this content
		# Redirect back to the list of active studies
		return HttpResponseRedirect(reverse('studies:active_studies'))

	# Get the groups for the study
	groups = Group.objects.filter(study=study)

	# Meta-data for user table (e.g., gender)
	# To add other data you are tracking for a participant see 'custom_auth' app
	# Initialize all dictionaries to convert integer keys to Strings that make sense here:
	gender_choices = {0: 'Female', 1: 'Male', 2: 'Other'}

	# Notes
	notes = Note.objects.filter(study=study, stage=None, group=None, group_stage=None, user_stage=None).order_by("timestamp").reverse()
	note_form = NoteForm()

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
def note_study(request, study_id):
	"""	Post a note on a study with ID study_id. """
	study = Study.objects.get(id=study_id)

	if not is_investigator(request.user, study):
		# The user is not allowed to view this content
		# Redirect back to the list of active studies
		return HttpResponseRedirect(reverse('studies:active_studies'))

	post_note(request, study)

	return HttpResponseRedirect(reverse('studies:investigator:study', args=[study_id]))


@login_required
def note_user_stage(request, study_id, user_id, stage_number):
	"""	Post a note on a user's stage_number'th stage. """
	study = Study.objects.get(id=study_id)

	if not is_investigator(request.user, study):
		# The user is not allowed to view this content
		# Redirect back to the list of active studies
		return HttpResponseRedirect(reverse('studies:active_studies'))

	# Get the participant and the 'stage_number' stage
	participant = User.objects.get(id=user_id)
	user_stage = UserStage.objects.get(user=participant, group_stage__order=stage_number, group_stage__stage__study=study)

	post_note(request, study, user_stage=user_stage)

	return HttpResponseRedirect(reverse('studies:investigator:user_stage', args=[study_id, user_id, stage_number]))


def post_note(request, study, stage=None, group_stage=None, user_stage=None):
	"""	Post a note. Helper function used to keep error handling in sync. """
	if request.method == 'POST':
		if request.POST['datum'] or request.FILES:
			# Need at LEAST contain datum OR an attachment
			form = NoteForm(request.POST, request.FILES)
			if form.is_valid():
				note = form.save(commit=False)
				note.user = request.user
				note.study = study
				if stage: note.stage = stage
				if group_stage: note.group_stage = group_stage
				if user_stage: note.user_stage = user_stage
				note.save()

				# Send email if specified
				if note.email:
					to_emails = []
					for user in study.investigators.all():
						to_emails.append(user.email)
					from_email = note.user.email
					subject = "New note from %s!" % note.user.username
					body = note.datum
					send_mail(subject, body, from_email, to_emails, fail_silently=False)



@login_required
def user_profile(request, study_id, user_id):
	""" Redirect to the user's first stage.
		TODO: In the future redirect to the user's first ~active~ stage instead. """
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

	# Get the participant and the 'stage_number' stage
	participant = User.objects.get(id=user_id)
	user_stage = UserStage.objects.get(user=participant, group_stage__order=stage_number, group_stage__stage__study=study)

	# Meta-data for the user profile goes here
	# To associate other meta-data with a participant see the 'custom_auth' app
	gender_choices = {0: 'Female', 1: 'Male', 2: 'Other'}
	
	# Get the data and notes associated with this stage
	data = Data.objects.filter(user_stage=user_stage).order_by("timestamp").reverse()
	notes = Note.objects.filter(user_stage=user_stage).order_by("timestamp").reverse()
	note_form = NoteForm()

	# For the sidebar:
	# Get all of the stages that the participant needs to complete for this study
	stages = UserStage.objects.filter(user=participant, group_stage__stage__study=study).order_by("group_stage__order")
	
	hide_title=True
	return render_to_response('investigator/data.html', locals(), context_instance=RequestContext(request))


@login_required
def advance_user(request, study_id, user_id, stage_number):
	"""	Advance a user with ID 'user_id' in the study with ID 'study_id':
		If the user's stage_number'th stage is active, complete it.
		If the user's stage_number'th stage is future, make it active. """
	if request.method == 'POST':
		# Get the participant and the 'stage_number' stage
		study = Study.objects.get(id=study_id)
		participant = User.objects.get(id=user_id)
		user_stage = UserStage.objects.get(user=participant, group_stage__order=stage_number, group_stage__stage__study=study)
		if user_stage.status == 1:
			# User stage is marked 'active': make complete
			user_stage.complete_stage()
		if user_stage.status == 2:
			# User stage is marked 'future': make active
			user_stage.start_stage()

	return HttpResponseRedirect(reverse('studies:investigator:user_stage', args=[study_id, user_id, stage_number]))



@login_required
def study_details(request, study_id):
	""" Display the details of the study with the ID 'study_id'. """
	request.session['study_id'] = study_id
	study = Study.objects.get(id=study_id)

	if not is_investigator(request.user, study):
		# The user is not allowed to view this content
		# Redirect back to the list of active studies
		return HttpResponseRedirect(reverse('studies:active_studies'))

	if request.method == 'POST':
		form = StudyForm(request.POST, instance=study)
		form.save()
		HttpResponseRedirect(reverse('studies:investigator:details', args=[study_id]))
	else:
		form = StudyForm(instance=study)

	return render_to_response('investigator/study_details.html', locals(), context_instance=RequestContext(request))


def send_email(request, study_id, group_id=None, user_id=None):
	study = Study.objects.get(id=study_id)
	if group_id is not None:
		to = Group.objects.get(id=group_id).name
	elif user_id is not None:
		to = User.objects.get(id=user_id).username
	else:
		to = Study.objects.get(id=study_id).name
	form = EmailForm()
	return render_to_response('investigator/email.html', locals(), context_instance=RequestContext(request))


def email_all(request, study_id):
	confirm = False #reset confirmation
	study = Study.objects.get(id=study_id)

	from_email = settings.EMAIL_HOST_USER
	from_name = settings.EMAIL_HOST_NAME

	to_name = 'All participants'
	to_emails = list()
	for group in Group.objects.filter(study=study):
		for user in group.users.all():
			to_emails.append(user.email)

	if request.method == 'POST':
		subject = request.POST['subject']
		body = request.POST['body']
		send_mail(subject, body, from_email, to_emails, fail_silently=False)
		confirm = True #show confirmation

	form = EmailForm()
	return render_to_response('investigator/email.html', locals(), context_instance=RequestContext(request))


def email_group(request, study_id, group_id):
	confirm = False #reset confirmation
	study = Study.objects.get(id=study_id)
	group = Group.objects.get(id=group_id)

	from_email = settings.EMAIL_HOST_USER
	from_name = settings.EMAIL_HOST_NAME

	to_name = group.name
	to_emails = list()
	for user in group.users.all():
		to_emails.append(user.email)

	if request.method == 'POST':
		subject = request.POST['subject']
		body = request.POST['body']
		send_mail(subject, body, from_email, to_emails, fail_silently=False)
		confirm = True #show confirmation

	form = EmailForm()
	return render_to_response('investigator/email.html', locals(), context_instance=RequestContext(request))


def email_user(request, study_id, user_id):
	confirm = False #reset confirmation
	study = Study.objects.get(id=study_id)
	participant = User.objects.get(id=user_id)
	to_name = participant.username
	from_email = settings.EMAIL_HOST_USER
	from_name = settings.EMAIL_HOST_NAME

	if request.method == 'POST':
		subject = request.POST['subject']
		body = request.POST['body']
		send_mail(subject, body, from_email, [participant.email], fail_silently=False)
		confirm = True #show confirmation

	form = EmailForm()
	return render_to_response('investigator/email.html', locals(), context_instance=RequestContext(request))


def export_as_csv(model, request, queryset, fields=None, exclude=None, header=True):
	""" Generic CSV export action """

	opts = model._meta
	field_names = set([field.name for field in opts.fields])
	many_to_many_field_names = set([many_to_many_field.name for many_to_many_field in opts.many_to_many])
	if fields:
		fieldset = set(fields)
		field_names = field_names & fieldset
	elif exclude:
		excludeset = set(exclude)
		field_names = field_names - excludeset

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')

	writer = csv.writer(response)
	if header:
		writer.writerow(list(chain(field_names, many_to_many_field_names)))
	for obj in queryset:
		row = []
		for field in field_names:
			row.append(unicode(getattr(obj, field)))
		for field in many_to_many_field_names:
			row.append(unicode(getattr(obj, field).all()))

		writer.writerow(row)
	return response


# Tables that we will be exporting
TABLES_TO_EXPORT = {
	1: Study,
	2: Stage,
	3: Group,
	4: GroupStage,
	5: UserStage,
	6: Data,
	7: Note,
}

# Link titles shown on the export page
TABLE_STRINGS_TO_EXPORT = {
	1: 'Study',
	2: 'Stages',
	3: 'Groups',
	4: 'Group Stages',
	5: 'User Stages',
	6: 'Data',
	7: 'Notes',
}


@login_required
def export(request, study_id):
	""" Display the details of the study with the ID 'study_id'. """
	request.session['study_id'] = study_id
	study = Study.objects.get(id=study_id)

	if not is_investigator(request.user, study):
		# The user is not allowed to view this content
		# Redirect back to the list of active studies
		return HttpResponseRedirect(reverse('studies:active_studies'))

	tables = TABLE_STRINGS_TO_EXPORT

	return render_to_response('investigator/export.html', locals(), context_instance=RequestContext(request))



@login_required
def export_table(request, study_id, table_num):
	""" Display the details of the study with the ID 'study_id'. """
	table_num = int(table_num)

	model = TABLES_TO_EXPORT[table_num]

	if table_num is 1:
		queryset = Study.objects.filter(id=study_id)
	elif table_num is 2:
		queryset = Stage.objects.filter(study__id=study_id)
	elif table_num is 3:
		queryset = Group.objects.filter(study__id=study_id)
	elif table_num is 4:
		queryset = GroupStage.objects.filter(group__study__id=study_id)
	elif table_num is 5:
		queryset = UserStage.objects.filter(group_stage__group__study__id=study_id)
	elif table_num is 6:
		queryset = Data.objects.filter(user_stage__group_stage__group__study__id=study_id)
	elif table_num is 7:
		queryset = Note.objects.filter(user_stage__group_stage__group__study__id=study_id)

	return export_as_csv(model, request, queryset)





