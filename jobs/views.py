

#All Django Imports
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

# @login_required
# def viewjob(request, jobid):
#     user = request.user
#     jobdetails = handler.getJobDetails()