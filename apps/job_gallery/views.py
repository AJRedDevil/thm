from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import apps.job_gallery.forms as jgforms
from apps.jobs.handler import JobManager
from thm.decorators import is_superuser


import simplejson as json

import logging
# Init Logger
logger = logging.getLogger(__name__)
# Create your views here.


@login_required
@is_superuser
def uploadJobPhotos(request, job_id):
    user = request.user
    if not user.is_staff:
        return redirect('home')
    jm = JobManager()
    job = jm.getJobDetails(job_id)
    if request.POST:
        logger.debug(request.POST)
        logger.debug(request.FILES)
        img_form = jgforms.JobGalleryImageForm(request.POST, request.FILES)
        if img_form.is_valid():
            img = img_form.save(commit=False)
            img.job = job
            img.save()
            logger.warn(request.FILES['image'])
            result = []
            filerecord = {}
            filerecord['name'] = request.FILES['image'].name
            filerecord['size'] = 'size'
            filerecord['url'] = 'url'
            filerecord['thumbnail_url'] = 'thumbnail_url'
            filerecord['delete_url'] = 'delete_url'
            filerecord['delete_type'] = 'delete_type'
            result.append(filerecord)
            responsedata = {}
            responsedata['files'] = result
            logger.warn(responsedata)
            return HttpResponse(
                json.dumps(responsedata), content_type="application/json",)

        if img_form.errors:
            logger.debug(
                "JobGalleryImageForm form has erorrs %s", img_form.errors)
            responsedata = dict(data=img_form.errors, success=False)
            return HttpResponse(
                json.dumps(responsedata), content_type="application/json", )

    responsedata = dict(success=False)
    return HttpResponse(
        json.dumps(responsedata),
        content_type="application/json", status=400)
