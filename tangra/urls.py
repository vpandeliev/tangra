from django.conf.urls import include, url
from django.contrib import admin

from tangra.views import *

# Import for the API
from public_api.views import DataView


urlpatterns = [
    url(r'^$', 'tangra.views.home', name='home'),
    url(r'^studies/', include('studies.urls', namespace='studies')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    
    #This is for the API:
    url(r'^api/post/', DataView.as_view()),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/auth/token/', 'rest_framework.authtoken.views.obtain_auth_token')
]
