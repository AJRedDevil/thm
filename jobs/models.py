

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from users.models import UserProfile


import jsonfield

# Create your models here.

STATUS_SELECTION = (('new','New'),('accepted','Accepted'),('completed','Completed'))

class Jobs(models.Model):

    ## Calculating delivery code before hand and inserting it as default so that it won't be tampered with.
    current_time = timezone.now

    customer = models.ForeignKey(UserProfile)
    fee = models.DecimalField(_('reward'), decimal_places=2, 
        max_digits=1000)
    status = models.TextField(_('status'), choices=STATUS_SELECTION, default='New')
    creation_date = models.DateTimeField(_('creation_date'), 
        default=current_time)
    handymen = models.TextField(_('shipper'), blank=True, null=True) 
    isaccepted = models.BooleanField(_('isaccepted'), default=False)
    isnotified = models.BooleanField(_('isnotified'), default=False)
    is_complete = models.BooleanField(_('is_complete'), default=False)
    ishidden = models.BooleanField(_('ishidden'), default=False)
    distance = models.DecimalField(_('distance'), decimal_places=2,
        max_digits=1000, default=0)
    completion_date = models.DateTimeField(_('completion_date'), 
        blank=True, null=True)
    available_handymen = jsonfield.JSONField(_('available_handymen'), default={})
    tracking_number = models.TextField(_('tracking_number'), blank=True)
    considered_handymen = models.TextField(_('considered_handymen'), default=[])

    def __unicode__(self):
        return str(self.id )

        #Overriding
    def save(self, *args, **kwargs):
        super(Jobs, self).save(*args, **kwargs)
