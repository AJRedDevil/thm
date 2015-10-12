

import datetime
import logging
import pytz
from django.conf import settings
from django.core import serializers
from django.db.models import Q
from django.shortcuts import get_object_or_404
from time import mktime
from django.utils import timezone
from django.utils.timezone import localtime

from .models import Jobs, JobEvents, JobScheduler
from apps.subscription.models import Subscriber

# Init Logger
logger = logging.getLogger(__name__)

EVENT_CLASSES = {
    '0' : 'event-special',
    '1' : 'event-info',
    '2' : 'event-important',
    "3" : 'event-success',
    '4' : 'event-warning',
    '5' : 'event-inverse'
}

class JobManager(object):
    """docstring for JobManager"""

    def getJobDetails(self, job_id):
        """List job information"""
        job = get_object_or_404(Jobs, jobref=job_id)
        if job.handyman.count():
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

        for job in jobs:
            try:
                scheduler = JobScheduler.objects.get(job=job, active=True)
                setattr(job, 'scheduler_id', scheduler.id)
                setattr(job, 'is_scheduled', True)
            except JobScheduler.DoesNotExist, err:
                setattr(job, 'is_scheduled', False)

        
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

    def createJobScheduler(self, job):
        """Creates Job Scheduler with default params
        """
        job_scheduler = JobScheduler(job=job)
        job_scheduler.save()

    def createJob(self, customer):
        """
        Creates a job request with default params
        """
        job = Jobs(customer=customer)
        job.save()
        job = self.getJobDetails(job.id)
        self.createJobScheduler(job)

    def getJobsInRange(self, _from, _to):
        """Returns all the job in specified time range
        """
        jobs=Jobs.objects.filter(Q(creation_date__range=(_from, _to)) | Q(inspection_date__range=(_from, _to)) | Q(accepted_date__range=(_from, _to)) |Q(completion_date__range=(_from, _to)))
        return set(jobs)

    @staticmethod
    def timestamp_to_datetime(timestamp):
        if isinstance(timestamp, (str, unicode)):
            tzinfo=pytz.timezone("Asia/Kathmandu")
            if len(timestamp) == 13:
                timestamp=int(timestamp)/1000
            return timezone.make_aware(timezone.datetime.fromtimestamp(timestamp), tzinfo)
        else:
            return ''

    @staticmethod
    def datetime_to_timestamp(_date):
        if isinstance(_date, datetime.datetime):
            timestamp=mktime(_date.timetuple())
            json_timestamp=int(timestamp)*1000
            return '{0}'.format(json_timestamp)
        else:
            return ""

    def __handle_new_rejected_discarded_job_for_calendar(self, job):
        start = job.creation_date
        end = job.creation_date + datetime.timedelta(hours=1)
        return (localtime(start), localtime(end))

    def __handle_inspection_job_for_calendar(self, job):
        job_scheduler = JobScheduler.objects.get(job=job)
        start = job_scheduler.inspection_start_date
        end = job_scheduler.inspection_end_date
        return (localtime(start), localtime(end))

    def __handle_accepted_completed_job_for_calendar(self, job):
        job_scheduler = JobScheduler.objects.get(job=job)
        start = job_scheduler.job_start_date
        end = job_scheduler.job_end_date
        return (localtime(start), localtime(end))

    def __get_start_end_datetime(self, job):
        if job.status in ['0', '4', '5']:
            return self.__handle_new_rejected_discarded_job_for_calendar(job)
        elif job.status == '1':
            return self.__handle_inspection_job_for_calendar(job)
        elif job.status in ['2', '3']:
            return self.__handle_accepted_completed_job_for_calendar(job)
        else:
            return ("", "")

    def get_jobs_for_calendar(self, _from, _to):
        """Returns all the jobs in range and their schedule
        """
        _from = JobManager.timestamp_to_datetime(_from)
        _to = JobManager.timestamp_to_datetime(_to)
        jobs = self.getJobsInRange(_from, _to)
        URL = getattr(settings, "URL", "")
        events=[]
        for job in jobs:
            start, end = self.__get_start_end_datetime(job)
            handymen = ', '.join([item.get('name') for item in job.handyman.values('name')])
            event = {
                "id":job.id,
                "title":"{0} : {1} - {2} ~~ {3}".format(job.id, job.customer, job.remarks, handymen),
                "url": URL + "jobs/{0}".format(job.jobref) if URL else "",
                "class": EVENT_CLASSES[job.status],
                "start": JobManager.datetime_to_timestamp(start),
                "end": JobManager.datetime_to_timestamp(end)
            }
            events.append(event)
        return events

    def activateJobScheduler(self, job):
        """Activates the job scheduler upon inspection
        """
        job_scheduler = JobScheduler.objects.get(job=job)
        job_scheduler.active = True
        job_scheduler.inspection_start_date = timezone.now()
        job_scheduler.inspection_end_date = timezone.now() + datetime.timedelta(hours=1)
        job_scheduler.save()

    def addCompletionToJobScheduler(self, job):
        """Updated the job scheduler with completion dates
        """
        job_scheduler = JobScheduler.objects.get(job=job)
        job_scheduler.job_start_date = job.accepted_date
        job_scheduler.job_end_date = job.accepted_date + datetime.timedelta(hours=4)
        job_scheduler.save()

    def deactivateJobScheduler(self, job):
        """
        """
        job_scheduler = JobScheduler.objects.get(job=job)
        job_scheduler.active = False
        job_scheduler.save()

    def getJobScheduler(self, scheduler_id):
        """Returns the job scheduler for that particular job
        """
        try:
            scheduler = JobScheduler.objects.get(id=scheduler_id)
            return scheduler
        except JobScheduler.DoesNotExist, err:
            logger.debug("Job Scheduler doesn't exist: ", err)
            return None

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
