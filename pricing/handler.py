

import collections
import logging


from .models import ComplexityRate, HourRate
# Init Logger
logger = logging.getLogger(__name__)

class PricingManager(object):
    """Handler for Pricing Model
    """
    def __init__(self):
        pass

    def getComplexityRate(self):
        """Returns all the complexity rates"""
        _complexity_rates = []
        complexity_rates = ComplexityRate.objects.all()
        for complexity_rate in complexity_rates:
            _complexity_rates.append(complexity_rate.complexity_rate)
        _complexity_rates = sorted(_complexity_rates, key=lambda x: float(x))
        return _complexity_rates

    def getHourRate(self):
        """Returns a dict of min. hours and their rate"""
        _hour_rates = {}
        hour_rates = HourRate.objects.all()
        for hour_rate in hour_rates:
            _hour_rates.update(hour_rate.hour_rate)
        _hour_rates = collections.OrderedDict(sorted(_hour_rates.iteritems(), key=lambda x: int(x[0])))
        return _hour_rates