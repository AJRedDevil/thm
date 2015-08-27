

#All Django Imports
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from thm.decorators import is_superuser
from .forms import JobCreationForm, JobCreationFormAdmin, JobEditFormAdmin
import apps.job_gallery.forms as jgforms
from .handler import JobManager
from apps.commcalc.handler import CommissionManager
from libs.sparrow_handler import Sparrow
from libs import out_sms as messages
import logging
# Init Logger
logger = logging.getLogger(__name__)


@login_required
@is_superuser
def createJob(request):
    user = request.user

    if request.method == "GET":
        job_form = JobCreationFormAdmin()
        return render(request, 'createjob.html', locals())
    if request.method == "POST":
        logger.debug(request.POST)
        job_form = JobCreationFormAdmin(request.POST)
        if job_form.is_valid():
            job_form.save()
            return redirect('home')
        if job_form.errors:
            logger.debug("Form has errors, %s ", job_form.errors)
            return render(request, 'createjob.html', locals())


@login_required
def viewJob(request, job_id):
    user = request.user
    jm = JobManager()
    job = jm.getJobDetails(job_id)
    jobstatus = int(job.status)
    job_before = job.gallery.filter(img_type=0)
    job_after = job.gallery.filter(img_type=1)
    if request.method == "POST" and user.is_superuser:
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
                return render(request, 'jobdetails.html', locals())
            # save the job with the details provided
            job_form.save()
            job = jm.getJobDetails(job_id)
            # if a job is set as accepted , update the accepted time
            # only update the accepted time once
            if job.status == '2' and job.accepted_date is None:
                job.accepted_date = timezone.now()
                job.save()
                vas = Sparrow()
                if len(job.handyman.all()) > 0:
                    msg = messages.JOB_ACCEPTED_MSG.format(
                        job.handyman.all()[0].name,
                        job.handyman.all()[0].phone.as_national
                    )
                    logger.warn(msg)
                    status = vas.sendMessage(msg, job.customer.primary_contact_person)
                    logger.warn("Message status \n {0}".format(status))
                # Notify the user that the job is accepted here.
                job = jm.getJobDetails(job_id)
                job_form = JobEditFormAdmin(instance=job)
                return redirect('home')
                # return render(request, 'jobdetails.html',locals())
            # if a job is set as complete , update the completion time
            # only update the completion time once
            if job.status == '3' and job.completion_date is None:
                job.completion_date = timezone.now()
                job.save()
                # Notify the user that the job is complete here.
                vas = Sparrow()
                msg = messages.JOB_COMPLETE_MSG.format(job.id)
                logger.warn(msg)
                status = vas.sendMessage(msg, job.customer.primary_contact_person)
                logger.warn("Message status \n {0}".format(status))
                job = jm.getJobDetails(job_id)
                job_form = JobEditFormAdmin(instance=job)
                # Add commission for that job
                cm = CommissionManager()
                cm.addCommission(job)
                return redirect('home')
                # return render(request, 'jobdetails.html',locals())
            return redirect('home')

        if job_form.errors:
            logger.debug("Form has errors, %s ", job_form.errors)

        return render(request, 'jobdetails.html', locals())

    if user.is_superuser:
        job_form = JobEditFormAdmin(instance=job)
        img_form = jgforms.JobGalleryImageForm()
        return render(request, 'jobdetails.html', locals())

    if user.is_staff:
        return render(request, 'jobdetails_hm.html', locals())

    return render(request, 'jobdetails_user.html', locals())
