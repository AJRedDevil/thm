
from django.utils import timezone
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Jobs, JobEvents
import logging
# Init Logger
logger = logging.getLogger(__name__)

class JobManager(object):
    """docstring for JobManager"""
    def getJobDetails(self, job_id):
        """List job information"""
        job = get_object_or_404(Jobs, id=job_id)
        return job


class JobEventManager(object):
    """docstring for UserEventManager"""
    
    def __init__(self):
        pass

    def getallevents(self, job):
        """Returns all the events of a job"""
        allevents = JobEvents.objects.filter(job=job.id)
        return allevents

    def getlatestevent(self, job):
        """Returns the latest event of the job"""
        event = JobEvents.objects.filter(job=job.id).order_by('-updated_on')[:1]
        return event

    def setevent(self, job, eventtype, extrainfo=None):
        """Sets the event for the job with the type given"""
        eventtype = int(eventtype)
        event = JobEvents(job=job, event=eventtype, extrainfo=extrainfo, updated_on=timezone.now())
        JobEvents.save(event)
        return "success"