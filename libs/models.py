from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from users.models import UserProfile

class SMSLog(models.Model):
    """
    Logs for all SMS sent out 
    """
    user = models.ForeignKey(UserProfile, related_name='sms')
    msg = models.TextField(_('msg'))
    time = models.DateTimeField(_('time'), default=timezone.now)


class SMSLogManager(object):
    """docstring for UserEventManager"""
    
    def __init__(self):
        pass

    def getAllSMS(self, user):
        """Returns all the sms of a user"""
        allsms = SMSLog.objects.filter(user=user)
        return allsms

    def getLatestSMS(self, user):
        """Returns the latest sms of the user"""
        sms = SMSLog.objects.filter(user=user.id).order_by('-time')[:1]
        return sms

    def updateLog(self, user, msg):
        """Updates log with the SMS data"""
        message_log = SMSLog(user=user, msg=msg)
        SMSLog.save(message_log)
        return "success"