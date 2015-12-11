

import json
import logging

#All Django Imports
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from thm.decorators import is_superuser
from .forms import JobCreationForm, JobCreationFormAdmin, JobEditFormAdmin, JobSchedulerCompleteForm, JobSchedulerInspectionForm
import apps.job_gallery.forms as jgforms
from .handler import JobManager
from apps.commcalc.handler import CommissionManager
from libs.sparrow_handler import Sparrow
from libs import out_sms as messages
# Init Logger
logger = logging.getLogger(__name__)

@login_required
@is_superuser
def createJob(request):
    user = request.user
    jm = JobManager()
    
    if request.method == "GET":
        job_form = JobCreationFormAdmin()
        return render(request, 'createjob.html', locals())
    if request.method == "POST":
        logger.debug(request.POST)
        job_form = JobCreationFormAdmin(request.POST)
        if job_form.is_valid():
            job=job_form.save()
            jm.createJobScheduler(job)
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
            if request.POST.get('status') == '3' and job.accepted_date is None:
                status_error = "Accept the job before completing it"
                return render(request, 'jobdetails.html', locals())
            # save the job with the details provided
            job_form.save()
            job = jm.getJobDetails(job_id)
            # if a job is set as accepted , update the accepted time
            # only update the accepted time once
            if job.status == '1' and job.inspection_date:
                jm.activateJobScheduler(job)
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
                jm.addCompletionToJobScheduler(job)
                job_form = JobEditFormAdmin(instance=job)
                return redirect('home')
                # return render(request, 'jobdetails.html',locals())
            # if a job is set as complete , update the completion time
            # only update the completion time once
            if job.status == '3':
                cm = CommissionManager()
                if job.completion_date is None:
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
                    cm.addCommission(job)
                else:
                    job = jm.getJobDetails(job_id)
                    job_form = JobEditFormAdmin(instance=job)
                    cm.updateCommission(job)
                return redirect('home')
                # return render(request, 'jobdetails.html',locals())
            # if a job is set as rejected or discarded, remove the comission
            if job.status == '4' or job.status == '5':
                cm = CommissionManager()
                job = jm.getJobDetails(job_id)
                job_form = JobEditFormAdmin(instance=job)
                cm.removeCommission(job)
                jm.deactivateJobScheduler(job)
                return redirect('home')
            return redirect('home')

        if job_form.errors:
            logger.debug("Form has errors, %s ", job_form.errors)

        return render(request, 'jobdetails.html', locals())

    if user.is_superuser:
        job_form = JobEditFormAdmin(instance=job)
        img_form = jgforms.JobGalleryImageForm()
        return render(request, 'jobdetails.html', locals())

    if user.user_type==1:
        return render(request, 'jobdetails_hm.html', locals())

    return render(request, 'jobdetails_user.html', locals())

@login_required
@is_superuser
def calendar(request):
    user = request.user
    return render(request, 'calendar.html', locals())

@login_required
@is_superuser
def events(request):
    user=request.user
    data_get_from=request.GET['from']
    data_get_to=request.GET['to']
    jm = JobManager()
    events = jm.get_jobs_for_calendar(data_get_from, data_get_to)
    data=dict(result=events, success=1)
    return HttpResponse(
        json.dumps(data),
        content_type="application/json")

@login_required
@is_superuser
def viewJobScheduler(request, job_scheduler_id):
    user=request.user
    jm = JobManager()
    job_scheduler = jm.getJobScheduler(job_scheduler_id)
    job = job_scheduler.job
    job_status = job.status
    if job_status == '1':
        job_scheduler_form = JobSchedulerInspectionForm(instance=job_scheduler)
    elif job_status in ['2', '3']:
        job_scheduler_form = JobSchedulerCompleteForm(instance=job_scheduler)
    return render(request, 'job_scheduler.html', locals())

@login_required
@is_superuser
def updateJobScheduler(request, job_scheduler_id):
    user = request.user
    jm = JobManager()
    job_scheduler = jm.getJobScheduler(job_scheduler_id)
    if request.method == 'POST':
        job = job_scheduler.job
        if job.status == '1':
            job_scheduler_form = JobSchedulerInspectionForm(request.POST, instance=job_scheduler)
        elif job.status in ['2', '3']    :
            job_scheduler_form = JobSchedulerCompleteForm(request.POST, instance=job_scheduler)
        if job_scheduler_form.is_valid():
            job_scheduler_form.save()
        if job_scheduler_form.errors:
            return render(request, 'job_scheduler.html', locals())
    return redirect('home')