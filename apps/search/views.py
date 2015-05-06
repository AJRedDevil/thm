from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from thm.decorators import is_superuser

from apps.users import handler as userhandler
from apps.users import forms as userforms
from libs.googleapi_handler import GMapPointWidget
import simplejson as json
import logging
import re
# Init Logger
logger = logging.getLogger(__name__)
# Create your views here.


@login_required
@is_superuser
def userSearch(request, phone=None):
    """
    Searches a user for the matching pattern and
    returns a list of matches
    """
    logging.warn(request.GET)

    if 'user' in request.GET:
        querystring = request.GET['user']
        um = userhandler.UserManager()
        result = um.getUserList(querystring)
        data = result.values('phone', 'name')
        data = json.loads(json.dumps(list(data)))
        responsedata = dict(detail=data)
        return HttpResponse(
            json.dumps(responsedata),
            content_type="application/json",
            status=200)

    return redirect('home')


@login_required
@is_superuser
def userSearchDetail(request):
    """
    Searches a user from the mobile number provided
    And lists their detail
    """
    if request.method == "POST":
        logger.debug(request.POST)
        phone = request.POST['phone']
        try:
            phone = re.findall('\((.*?)\)', phone)[-1]
        except Exception:
            return redirect('home')
        um = userhandler.UserManager()
        customer = um.getUserDetailsFromPhone(phone)
        return redirect('editUserDetail', userref=customer.userref)
    return redirect('home')

