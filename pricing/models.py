


import jsonfield


from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django.db import models

# Create your models here.

TIME_UNIT_SELECTION = (
    ('0', 'Hours'),
    ('1', 'Days')
)

COMPLEXITY_SELECTION = (
    ('0', '1'),
    ('1', '2'),
    ('2', '3'),
    ('3', '4'),
    ('4', '5')
)


class ComplexityRate(models.Model):
    """ComplexityRate model for defining rates

    Use Case [Lower -> Higher]
        1 - x
        2 - 2x
        3 - 3x
        4 - 4x
        5 - 5x
    """
    complexity_rate = models.CharField(
        _('complexity_rate'),
        max_length=1, choices=COMPLEXITY_SELECTION, default='0')
    complexity_rate = models.IntegerField(
        _('complexity_rate'), max_length=2, default=1)

    def save(self, *args, **kwargs):
        super(ComplexityRate, self).save(*args, **kwargs)


class HourRate(models.Model):
    """HourRate model for defining hourly rates

    Use Case - Min. hrs before new set of rates
    2   - 6x
    5   - 5x
    8   - 4x
    12  - 3x
    16  - 2x
    24  - x
    """
    hour_rate = jsonfield.JSONField(
        _('hour_rate'), default='{}', max_length=9999)

    def save(self, *args, **kwargs):
        super(HourRate, self).save(*args, **kwargs)


class PricingModel(models.Model):
    """Pricing Model to estimate price"""
    time_unit_selection = models.CharField(
        _('time_unit_selection'),
        max_length=1,
        choices=TIME_UNIT_SELECTION,
        default='0'
    )
    estimated_time = models.DecimalField(
        _('estimated_time'),
        decimal_places=2,
        max_digits=100,
        default=1.0
    )
    complexity = models.CharField(
        _('complexity'),
        max_length=1,
        choices=COMPLEXITY_SELECTION,
        default='0'
    )
    # complexity = models.IntegerField(_('complexity'), max_length=2, default=1)
    discount = models.DecimalField(
        _('discount'),
        decimal_places=2,
        max_digits=100,
        default=0
    )

    def save(self, *args, **kwargs):
        super(PricingModel, self).save(*args, **kwargs)
