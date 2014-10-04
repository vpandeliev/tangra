from django.conf.urls import patterns, url
from investigator.views import *

urlpatterns = patterns('',
	url(r'^(\d+)/$', show_study, name='study'),
)