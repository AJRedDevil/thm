
from django.utils import timezone
from django.http import Http404

from .models import UserEvents, UserProfile


class UserManager(object):
    """docstring for UserManager"""
    def getUserDetails(user_id):
        """List user information"""
        try:
            user = UserProfile.objects.get(id=user_id, is_active=True)
        except UserProfile.DoesNotExist:
            raise Http404
        return user

class UserEventManager(object):
    """docstring for UserEventManager"""
    
    def __init__(self):
        pass

    def getallevents(self, user):
        """Returns all the events of a user"""
        allevents = UserEvents.objects.filter(questr=user.id)
        return allevents

    def getlatestevent(self, user):
        """Returns the latest event of the user"""
        event = UserEvents.objects.filter(questr=user.id).order_by('-updated_on')[:1]
        return event

    def setevent(self, user, eventtype, extrainfo=None):
        """Sets the event for the user with the type given"""
        eventtype = int(eventtype)
        event = UserEvents(user=user, event=eventtype, extrainfo=extrainfo, updated_on=timezone.now())
        UserEvents.save(event)
        return "success"