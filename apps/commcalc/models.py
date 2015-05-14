

from django.db import models
from djmoney.models.fields import MoneyField
from django.utils.translation import ugettext_lazy as _

from apps.jobs.models import Jobs
from apps.users.models import UserProfile
# Create your models here.


class Commission(models.Model):
    """
    Commission models
    """
    job = models.ForeignKey(
        Jobs,
        related_name='commission'
    )
    amount = MoneyField(
        _('amount'),
        decimal_places=2,
        max_digits=8,
        blank=True,
        null=True,
        default_currency='NPR',
        default=0.00
    )
    handyman = models.ForeignKey(
        UserProfile,
        related_name='handyman'
    )
    is_paid = models.BooleanField(_('Paid'), default=False)
