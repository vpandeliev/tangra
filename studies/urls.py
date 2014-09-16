from django.conf.urls import patterns, url
from studies.views import *

urlpatterns = patterns('',
	url(r'^$', show_active_studies, name='active_studies'),
	url(r'^(\d+)/$', show_study, name='study'),
)