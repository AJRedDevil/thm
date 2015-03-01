

#All Django Imports
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from thm.decorators import is_superuser
from .forms import JobCreationForm, JobCreationFormAdmin, JobEditFormAdmin
from .handler import JobManager
from libs.sparrow_handler import Sparrow
from libs import out_sms as messages
import logging
# Init Logger
logger = logging.getLogger(__name__)


@login_required
@is_superuser
def createJob(request):
    user = request.user

    if request.method == "POST":
        logger.debug(request.POST)
        job_form = JobCreationFormAdmin(request.POST)
        if job_form.is_valid():
            job_form.save()
            return redirect('home')

        if job_form.errors:
            logger.debug("Form has errors, %s ", job_form.errors)

    job_form = JobCreationFormAdmin()
    return render(request, 'createjob.html', locals())

@login_required
@is_superuser
def viewJob(request, job_id):
    user = request.user
    jm = JobManager()
    job = jm.getJobDetails(job_id)
    if request.method=="POST":
        logger.debug(request.POST)
        job_form = JobEditFormAdmin(request.POST, instance=job)
        if job_form.is_valid():
            # Job escalation moves one way and cannot be backward,
            # that means if a job's status is set as accepted it cannot be
            # reverted to New, further if it's set as Complete, it cannot be set
            # as Accepted or New
            job = jm.getJobDetails(job_id)
            if int(job_form.cleaned_data['status']) < int(job.status):
                job_form = JobEditFormAdmin(instance=job)
                return render(request, 'jobdetails.html',locals())
            # save the job with the details provided
            job_form.save()
            job = jm.getJobDetails(job_id)
            # if a job is set as accepted , update the accepted time
            # only update the accepted time once
            if job.status=='1' and job.accepted_date == None:
                job.accepted_date= timezone.now()
                job.save()
                vas = Sparrow()
                if len(job.handyman.all()) > 0:
                    msg = messages.JOB_ACCEPTED_MSG.format(
                        job.handyman.all()[0].name,
                        job.handyman.all()[0].phone.as_international
                    )
                    logger.warn(msg)
                    status = vas.sendMessage(msg, job.customer)
                    logger.warn("Message status \n {0}".format(status))
                # Notify the user that the job is accepted here.
                job = jm.getJobDetails(job_id)
                job_form = JobEditFormAdmin(instance=job)
                return render(request, 'jobdetails.html',locals())
            # if a job is set as complete , update the completion time
            # only update the completion time once
            if job.status=='2' and job.completion_date == None:
                job.completion_date= timezone.now()
                job.save()
                vas = Sparrow()
                msg = messages.JOB_COMPLETE_MSG.format(job.id,job.get_jobtype_display())
                logger.warn(msg)
                status = vas.sendMessage(msg, job.customer)
                logger.warn("Message status \n {0}".format(status))
                # Notify the user that the job is complete here.
                job = jm.getJobDetails(job_id)
                job_form = JobEditFormAdmin(instance=job)
                return render(request, 'jobdetails.html',locals())

        if job_form.errors:
            logger.debug("Form has errors, %s ", job_form.errors)

    job_form = JobEditFormAdmin(instance=job)
    return render(request, 'jobdetails.html',locals())
