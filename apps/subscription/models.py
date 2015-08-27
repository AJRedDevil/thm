

import datetime
import pytz
import logging
from django.db import models
from djmoney.models.fields import MoneyField
from django.utils import timezone
from django.utils .translation import ugettext_lazy as _

from apps.users.models import UserProfile

# Create your models here.

class SubscriptionPackage(models.Model):
    """Packages for subscription
    """
    name = models.CharField(
        _('name'),
        max_length=100,
        default="",
        blank=False,
        unique=True
        )
    price = MoneyField(
        _('price'),
        decimal_places=2,
        max_digits=8,
        blank=False,
        null=False,
        default_currency='NPR',
        default=0.0
        )
    max_repair = models.IntegerField(
        _('max_repair'),
        max_length=3,
        default=0
        )
    discount = models.DecimalField(
        _('discount'),
        decimal_places=2,
        max_digits=100,
        default=0.0
        )

    def __unicode__(self):
        return self.name

class Subscriber(models.Model):
    """All the subscriber list
    """
    primary_contact_person = models.ForeignKey(
        UserProfile,
        related_name='primaryContactPerson'
        )
    secondary_contact_person = models.ForeignKey(
        UserProfile,
        related_name='secondaryContactPerson'
        )
    subscriber_name = models.CharField(
        _('subscriber_name'),
        max_length=100,
        default="",
        blank=False,
        null=False
        )
    office_number = models.IntegerField(
        _('office_number'),
        max_length=7,
        default=0,
        blank=False,
        null=False
        )
    is_office=models.BooleanField(
        _('is_office'),
        default=False
        )

    def __unicode__(self):
        return self.subscriber_name

class Subscription(models.Model):
    """Subscription to specific package
    """
    start_date = models.DateField(
        _('start_date'),
        blank=True,
        null=False
    )
    end_date = models.DateField(
        _('end_date'),
        blank=True,
        null=False
    )
    package = models.ForeignKey(
        SubscriptionPackage,
        null=False,
        related_name="packageSelected"
    )
    terminated = models.BooleanField(
        _('terminated'),
        default=False
    )
    terminated_date = models.DateField(
        _('end_date'),
        blank=True,
        null=True
    )
    subscriber = models.ForeignKey(
        Subscriber,
        null=False,
        related_name="subscriber"
    )
    repairs_completed = models.IntegerField(
        _('repairs_completed'),
        max_length=1000,
        default=0,
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if self.terminated:
            from apps.jobs.models import Jobs
            ending_date = timezone.now().date() + datetime.timedelta(days=1)
            self.terminated_date = ending_date
            starting_date=pytz.timezone("Asia/Kathmandu").localize(datetime.datetime.combine(self.start_date,datetime.time(0,0)),is_dst=None)
            ending_date=pytz.timezone("Asia/Kathmandu").localize(datetime.datetime.combine(ending_date,datetime.time(0,0)), is_dst=None)
            self.repairs_completed = Jobs.objects.filter(completion_date__range=[starting_date, ending_date], customer=self.subscriber).count()

        super(Subscription, self).save(*args, **kwargs)

    