

#All Django Imports
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from thm.decorators import is_superuser
from .forms import JobCreationForm, JobCreationFormAdmin, JobEditFormAdmin
from .handler import JobManager
import logging
# Init Logger
logger = logging.getLogger(__name__)


@login_required
@is_superuser
def createJob(request):
    user = request.user

    if request.method == "POST":
        job_form = JobCreationFormAdmin(request.POST)
        if job_form.is_valid():
            logger.debug("form is correct")
            job_form.save()

        if job_form.errors:
            logger.debug("Form has errors, %s ", job_form.errors)

    job_form = JobCreationFormAdmin()
    return render(request, 'createjob.html',locals())

@login_required
@is_superuser
def viewJob(request, job_id):
    user = request.user
    jm = JobManager()
    job = jm.getJobDetails(job_id)
    if request.method=="POST":
        job_form = JobEditFormAdmin(request.POST)
        if job_form.is_valid():
            job = jm.getJobDetails(job_id)
            job_form = JobEditFormAdmin(request.POST, instance=job)
            job_form.save()

        if job_form.errors:
            logger.debug("Form has errors, %s ", job_form.errors)

    job_form = JobEditFormAdmin(instance=job)
    return render(request, 'jobdetails.html',locals())
