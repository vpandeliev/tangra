from django.conf.urls import patterns, url
from investigator.views import *

urlpatterns = patterns('',

	# Overview of each group/participant's progress in the study
	url(r'^(\d+)/$', show_study, name='study'),

	# Email everyone in the study
	url(r'^(\d+)/email/$', email_all, name='email_all'),

	# Add note to study
	url(r'^(\d+)/note/$', note_study, name='note_study'),

	# Email everyone in a group
	url(r'^(\d+)/group/(\d+)/email/$', email_group, name='email_group'),

	# View the details of the study (i.e., description, consent, etc.)
	url(r'^(\d+)/details/$', study_details, name='details'),
        
        # View the data.
        url(r'^(\d+)/view_data/$', view_data, name='view_data'),

	# Export all of the study data
	url(r'^(\d+)/export/$', export, name='export'),

	# Export a table of the study data
	url(r'^(\d+)/export/(\d+)/$', export_table, name='export_table'),

	# The user's profile (redirects to user_stage)
	url(r'^(\d+)/user/(\d+)/$', user_profile, name='user'),

	# Email the participant
	url(r'^(\d+)/user/(\d+)/email/$', email_user, name='email_user'),

	# Showing the data for a user's stage
	url(r'^(\d+)/user/(\d+)/stage/(\d+)/$', user_stage, name='user_stage'),

	# Add a note to a user's stage
	url(r'^(\d+)/user/(\d+)/stage/(\d+)/note/$', note_user_stage, name='note_user_stage'),

	# Add data to a user's stage
	#url(r'^(\d+)/user/(\d+)/stage/(\d+)/note/$', add_data, name='add_data'),

	# Advance a user
	url(r'^(\d+)/user/(\d+)/stage/(\d+)/advance/$', advance_user, name='advance_user'),
)
