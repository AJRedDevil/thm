from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers

from users import handler as userhandler
import simplejson as json
import logging

# Create your views here.


def userSearch(request, phone=None):
    """
    Searches a user for the matching pattern and
    returns a list of matches
    """
    user = request.user
    logging.warn(request.GET)
    if not user.is_authenticated():
        return redirect('home')

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


def userSearchDetail(request, phone=None):
    """
    Searches a user from the mobile number provided
    And lists their detail
    """
    if phone is not None:
        pass
    return redirect('home')
