from django.conf.urls import patterns, url
from investigator.views import *

urlpatterns = patterns('',
	url(r'^(\d+)/$', show_study, name='study'),
	url(r'^(\d+)/user/(\d+)/$', user_profile, name='user'),
	url(r'^(\d+)/user/(\d+)/stage/(\d+)/$', user_stage, name='user_stage'),
)
