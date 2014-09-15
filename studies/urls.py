from django.conf.urls import patterns, url
from studies.views import *

urlpatterns = patterns('',
	url(r'^$', show_many_studies, name='show_many_studies'),
	url(r'^(\d+)/$', show_one_study, name='show_one_study'),
)