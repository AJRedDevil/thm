from django.shortcuts import render, redirect
import job_gallery.forms as jgforms
from jobs.handler import JobManager

import logging
# Init Logger
logger = logging.getLogger(__name__)
# Create your views here.


def uploadBeforeJobPics(request, job_id):
    user = request.user
    if not user.is_staff:
        return redirect('home')
    jm = JobManager()
    job = jm.getJobDetails(job_id)
    if request.POST:
        logger.debug(request.POST)
        img_form = jgforms.JobGalleryImageForm(request.POST, request.FILES)
        if img_form.is_valid():
            img = img_form.save(commit=False)
            img.job = job
            img.save()

        if img_form.errors:
            logger.debug("JobGalleryImageForm form has erorrs %s", img_form.errors)
            return render(request, "uploadjobphotos.html", locals())

    img_form = jgforms.JobGalleryImageForm()
    return render(request, "uploadjobphotos.html", locals())
