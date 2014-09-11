from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def show_many_studies(request):
	return HttpResponse("Many studies lie here.")