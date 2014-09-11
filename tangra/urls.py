from django.conf.urls import include, url
from django.contrib import admin

from tangra.views import *

urlpatterns = [
    url(r'^$', 'tangra.views.home', name='home'),
    url(r'^studies/', include('studies.urls', namespace='studies')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
]
