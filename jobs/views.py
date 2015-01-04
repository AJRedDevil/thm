

#All Django Imports
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from thm.decorators import is_superuser
from .forms import JobCreationForm, JobCreationFormAdmin, JobEditFormAdmin
from .handler import JobManager
# @login_required
# def viewjob(request, jobid):
#     user = request.user
#     jobdetails = handler.getJobDetails()

@login_required
@is_superuser
def createJob(request):
    user = request.user

    if request.method == "POST":
        job_form = JobCreationFormAdmin(request.POST)
        if job_form.is_valid():
            job_form.save()
    
    job_form = JobCreationFormAdmin()
    return render(request, 'createjob.html',locals())

@login_required
@is_superuser
def viewJob(request, job_id):
    user = request.user
    jm = JobManager()
    job = jm.getJobDetails(job_id)
    job_form = JobEditFormAdmin(instance=job)
    return render(request, 'jobdetails.html',locals())

