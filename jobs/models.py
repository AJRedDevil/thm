

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django.contrib.gis.db import models

from users.models import UserProfile

import jsonfield
import uuid

from djmoney.models.fields import MoneyField
# Create your models here.

# Job Statuses
STATUS_SELECTION = (
    ('0', 'New'),
    ('1', 'Accepted'),
    ('3', 'Inspection'),
    ('2', 'Completed'),
    ('4', 'Rejected'),
    ('5', 'Discarded'),
)

# Type of jobs
JOBS_SELECTION = (
    ('0', 'N/A'),
    ('1', 'Plumbing'),
    ('2', 'Electrical'),
    ('3', 'Furnishing'),
    ('4', 'Masonry'),
)


# Returns a hash that is used as identifier for jobs
def getUniqueUUID():
    uniqueID = ''.join(str(uuid.uuid4()).split('-'))
    return uniqueID


class Jobs(models.Model):
    """
    The jobs model
    """
    # reference id for jobs
    # not the primary key though
    jobref = models.CharField(
        _('jobref'),
        max_length=100, unique=True, default=getUniqueUUID)
    # Customer's usertype is 2 so limiting the choices
    customer = models.ForeignKey(
        UserProfile,
        limit_choices_to={'user_type': '2'},
        related_name='jobs')
    fee = MoneyField(
        _('fee'),
        decimal_places=2,
        max_digits=8,
        blank=True,
        null=True,
        default_currency='NPR',
        default=0.00)
    status = models.CharField(
        _('status'),
        max_length=1,
        choices=STATUS_SELECTION,
        default='0',)
    creation_date = models.DateTimeField(
        _('creation_date'),
        default=timezone.now)
    jobtype = models.CharField(
        _('jobtype'),
        max_length=250,
        default='0',)
    handyman = models.ManyToManyField(UserProfile, related_name='orders')
    # jobs that are deleted or are to be purged would have this flag
    # set as true, no data would be permanently removed
    ishidden = models.BooleanField(_('ishidden'), default=False)
    # distance = models.DecimalField(
    #     _('distance'),
    #     decimal_places=2,
    #     max_digits=1000, default=0)
    accepted_date = models.DateTimeField(
        _('accepted_date'),
        blank=True, null=True, editable=False)
    completion_date = models.DateTimeField(
        _('completion_date'),
        blank=True, null=True, editable=False)
    # available_handymen = jsonfield.JSONField(
    #     _('available_handymen'), default={})
    # considered_handymen = models.TextField(_('considered_handymen'), default=[])
    remarks = models.TextField(_('remarks'), blank=False)
    # location / coordinates of the exact jobsite
    location = models.PointField(srid=4326, blank=True, null=True)
    # location / landmark near the jobsite
    location_landmark = models.CharField(
        _('Nearest Address'),
        max_length=100,
        blank=True
    )
    objects = models.GeoManager()

    def __unicode__(self):
        return str(self.jobref)

        #Overriding
    def save(self, *args, **kwargs):
        # set a unique ID for each jobs
        if self.jobref == '':
            self.jobref = ''.join(str(uuid.uuid4()).split('-'))

        # if no location is provided while creating the job
        # user the customer's default home location
        if self.location == '' or self.location is None:
            self.location = self.customer.address_coordinates

        super(Jobs, self).save(*args, **kwargs)


class JobEvents(models.Model):
    """Models for JobEvents"""

    job = models.ForeignKey(Jobs)
    event = models.IntegerField(_('event'), max_length=2, default=1)
    updated_on = models.DateTimeField(
        _('updated_on'),
        default=timezone.now)
    extrainfo = jsonfield.JSONField(
        _('extrainfo'), default='{}', max_length=9999)

    def save(self, *args, **kwargs):
        super(JobEvents, self).save(*args, **kwargs)
