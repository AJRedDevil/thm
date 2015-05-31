

import json
import logging
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render

from thm.decorators import is_superuser
from apps.pricing.forms import PricingForm
from .handler import PricingManager

logger = logging.getLogger(__name__)

# Create your views here.

WORKING_DAY = 8
HOURLY_PRICE = [350.0, 300.0]
DAILY_BALANCE = [400.0, 480.0]
COMPLEXITY_RATE = [1.0, 1.2]



# def __get_estimated_price(total_estimated_hours, complexity, discount):
#     """Returns the estimated price"""
#     total_estimated_price = 0.0
#     pm = PricingManager()
#     complexity_rates = pm.getComplexityRate()
#     hour_rates = pm.getHourRate()

#     complexity_rate = float(complexity_rates[int(complexity)])
#     hour_rate = hour_rates[hour_rates.keys()[-1]]
#     hour_rate_keys = [float(key) for key in hour_rates.keys()]
#     for key in hour_rate_keys:
#         if total_estimated_hours <= key:
#             hour_rate = hour_rates[str(key)]
#             break
#     total_estimated_price = (
#         complexity_rate + hour_rate) * total_estimated_hours

#     if discount:
#         total_estimated_price *= (1 - (discount / 100.0))

#     total_estimated_price = format(total_estimated_price, ',.2f')
#     return total_estimated_price

def __get_estimated_price(total_estimated_hours, complexity, discount):
    """Returns the estimated price"""
    total_estimated_price = 0.0

    index = int(complexity)
    hourly_rate = HOURLY_PRICE[0] if total_estimated_hours < 5  else HOURLY_PRICE[1]
    complexity_rate = COMPLEXITY_RATE[index]

    daily_balance  = (DAILY_BALANCE[index] * int(total_estimated_hours / 8) )

    if total_estimated_hours < 5:
        total_estimated_price = hourly_rate * complexity_rate * total_estimated_hours
    else:
        total_estimated_price = hourly_rate * complexity_rate * total_estimated_hours - daily_balance

    if discount:
        total_estimated_price *= (1 - (discount / 100.0))

    total_estimated_price = format(total_estimated_price, ',.2f')
    return total_estimated_price


@login_required
@is_superuser
def viewPricing(request):
    """View to show current rates and calculate estimated Price"""
    user = request.user
    pf = PricingForm()
    pricing_estimated = {"estimated_price": 0.0}
    if request.method == 'POST':
        time_unit = int(request.POST['time_unit_selection'])
        estimated_time = float(request.POST['estimated_time'])
        complexity_rate = request.POST['complexity']
        discount = float(request.POST['discount'])
        pf = PricingForm(request.POST)
        if pf.is_valid():
            total_estimated_hours = estimated_time if not time_unit else (
                estimated_time * WORKING_DAY)
            estimated_price = __get_estimated_price(
                total_estimated_hours, complexity_rate, discount)
            pricing_estimated["estimated_price"] = estimated_price
            return HttpResponse(
                json.dumps(pricing_estimated), content_type='application/json')
        if pf.errors:
            logger.debug("Form has errors, %s ", pf.errors)
    return render(request, 'pricing.html', locals())
