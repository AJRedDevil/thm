
from django.utils import timezone
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import UserEvents, UserProfile, UserToken
from libs.sparrow_handler import Sparrow
import logging
# Init Logger
logger = logging.getLogger(__name__)

class UserManager(object):
    """docstring for UserManager"""
    def getUserDetails(self, user_id):
        """List user information"""
        user = get_object_or_404(UserProfile, id=user_id, is_active=True)
        return user

    def sendVerfText(self, user_id):
        user = self.getUserDetails(user_id)
        token = UserToken.objects.get(user_id=user, status=False)
        vas = Sparrow()
        msg = "Thankyou for signing up with The Right Handyman, to complete registration, type VERIFYHM {0} and send to 2200.".format(token.get_vrfcode())
        logger.warn(msg)
        status = vas.sendMessage(msg, user)
        return status

    def sendVerfTextApp(self, user_id):
        user = self.getUserDetails(user_id)
        token = UserToken.objects.get(user_id=user, status=False)
        vas = Sparrow()
        msg = "{0}".format(token.get_vrfcode())
        status = vas.sendMessage(msg, user)
        return status

class UserEventManager(object):
    """docstring for UserEventManager"""
    
    def __init__(self):
        pass

    def getallevents(self, user):
        """Returns all the events of a user"""
        allevents = UserEvents.objects.filter(user=user.id)
        return allevents

    def getlatestevent(self, user):
        """Returns the latest event of the user"""
        event = UserEvents.objects.filter(user=user.id).order_by('-updated_on')[:1]
        return event

    def setevent(self, user, eventtype, extrainfo=None):
        """Sets the event for the user with the type given"""
        eventtype = int(eventtype)
        event = UserEvents(user=user, event=eventtype, extrainfo=extrainfo, updated_on=timezone.now())
        UserEvents.save(event)
        return "success"