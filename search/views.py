from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required


from users import handler as userhandler
from libs.googleapi_handler import GMapPointWidget
import simplejson as json
import logging
import re
# Init Logger
logger = logging.getLogger(__name__)
# Create your views here.


@login_required
def userSearch(request, phone=None):
    """
    Searches a user for the matching pattern and
    returns a list of matches
    """
    user = request.user
    logging.warn(request.GET)
    if not user.is_superuser:
        return redirect('home')

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
def userSearchDetail(request):
    """
    Searches a user from the mobile number provided
    And lists their detail
    """
    user = request.user

    if not user.is_superuser:
        return redirect('home')

    if request.method == "POST":
        logger.debug(request.POST)
        phone = request.POST['phone']
        phone = re.findall('\((.*?)\)', phone)[-1]
        um = userhandler.UserManager()
        customer = um.getUserDetailsFromPhone(phone)
        job = um.getLatestOrderDetails(customer)
        return render(request, 'userdetails.html', locals())
    return redirect('home')
