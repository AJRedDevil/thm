

import logging
from django.core import serializers
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Jobs, JobEvents
from apps.subscription.models import Subscriber

# Init Logger
logger = logging.getLogger(__name__)


class JobManager(object):
    """docstring for JobManager"""
    def getJobDetails(self, job_id):
        """List job information"""
        job = get_object_or_404(Jobs, jobref=job_id)
        setattr(job, 'commission_due', "Rs.{:,.2f}".format((0.2 * float(job.fee.amount))/job.handyman.count()))
        return job

    # def getJobsForHandyman(self, user):
    #     jobs = jobs.objects.filter(handyman!=None)

    def getAllJobs(self, user):
        if user.user_type == 0:
            jobs = Jobs.objects.filter()
        ## If it's a handymen, only show requests which they were assigned to
        elif user.user_type == 1:
            alljobs = Jobs.objects.exclude(handyman=None)
            # get the jobs where the handyman is listed
            # as the one chosen for the particular work
            jobs = [x for x in alljobs if user in x.handyman.all()]
            for job in jobs:
                setattr(job, 'commission_due', (0.2 * float(job.fee.amount))/job.handyman.count())
        ## If it's a customer only show requests that they created
        elif user.user_type == 2:
            jobs=[]
            subscribers=Subscriber.objects.filter(primary_contact_person=user)
            for subscriber in subscribers:
                jobs.extend(Jobs.objects.filter(customer_id=subscriber.id))
        else:
            jobs = []

        logger.debug("Job Details : \n {0}".format(
            serializers.serialize('json', jobs))
        )
        return jobs

    def getAllJobsByDate(self, user, date):
        """
        Returns list of jobs by date
        """
        if user.user_type == 0:
            jobs = Jobs.objects.filter(creation_date__gte=date)
        ## If it's a handymen, only show requests which they were assigned to
        elif user.user_type == 1:
            alljobs = Jobs.objects.filter(creation_date__gte=date).exclude(handyman=None)
            jobs = [x for x in alljobs if user in x.handyman.all()]
        ## If it's a customer only show requests that they created
        elif user.user_type == 2:
            jobs=[]
            subscribers=Subscriber.objects.filter(primary_contact_person=user)
            for subscriber in subscribers:
                jobs.extend(Jobs.objects.filter(customer_id=subscriber.id, creation_date__gte=date))
        else:
            jobs = []

        logger.debug("Job Details : \n {0}".format(serializers.serialize('json',jobs)))
        return jobs

    def createJob(self, customer):
        """
        Creates a job request with default params
        """
        job = Jobs(customer=customer)
        job.save()

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
