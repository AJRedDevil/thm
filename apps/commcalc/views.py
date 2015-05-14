

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from thm.decorators import is_superuser
from .forms import CommissionForm
from .handler import CommissionManager

import simplejson as json
import logging
# Init Logger
logger = logging.getLogger(__name__)
# Create your views here.


@login_required
@is_superuser
def viewCommission(request):
    """View to show current commission due for handyman"""
    user = request.user
    commission_form = CommissionForm()
    commission = {"commission": 0.0}
    if request.method == 'POST':
        logger.debug(request.POST)
        commission_form = CommissionForm(request.POST)
        if commission_form.is_valid():
            handyman = commission_form.cleaned_data['handyman']
            cm = CommissionManager()
            commission_earned = cm.getCommUser(handyman)
            commission["commission"] = commission_earned
            logger.warn(json.dumps(commission))
            return HttpResponse(
                json.dumps(commission), content_type='application/json')
        if commission_form.errors:
            logger.debug("Form has errors, %s ", commission_form.errors)
    return render(request, 'commission.html', locals())
