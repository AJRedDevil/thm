
from django.utils import timezone
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import UserEvents, UserProfile, UserToken, EarlyBirdUser
from libs.sparrow_handler import Sparrow
from libs import out_sms as messages

from phonenumber_field.modelfields import PhoneNumber
import logging
import os
# Init Logger
logger = logging.getLogger(__name__)


class UserManager(object):
    """docstring for UserManager"""
    def getUserDetails(self, user_id):
        """List user information"""
        user = get_object_or_404(UserProfile, id=user_id, is_active=True)
        return user

    def getUserDetailsFromPhone(self, phone):
        """List user information from phone number"""
        try:
            user_phone = PhoneNumber.from_string(phone)
            user = UserProfile.objects.get(phone=user_phone)
            return user
        except UserProfile.DoesNotExist:
            return None

    def sendVerfText(self, user_id):
        """Sends a verification text to the user"""
        user = self.getUserDetails(user_id)
        token = UserToken.objects.get(user_id=user, status=False)
        vas = Sparrow()
        msg = messages.PHONE_VERF_MSG.format(token.get_vrfcode())
        logger.debug(msg)
        status = vas.sendMessage(msg, user)
        return status

    def sendVerfTextApp(self, user_id):
        """Sends only the verification code, this is to be used from app"""
        user = self.getUserDetails(user_id)
        token = UserToken.objects.get(user_id=user, status=False)
        vas = Sparrow()
        msg = messages.PHONE_VERF_MSG.format(token.get_vrfcode())
        logger.debug(msg)
        status = vas.sendMessage(msg, user)
        return status

    def checkVerfCode(self, user, verf_code):
        """Checks if the user provided code is true"""
        try:
            token = UserToken.objects.get(user_id=user.id, status=False)
        except Exception:
            return False
        if token.is_alive:
            if token.get_vrfcode() == verf_code:
                return True
            else:
                return False
        return False

    def checkPasswdVerfCode(self, user, verf_code):
        """Checks if the user provided code is true"""
        try:
            token = UserToken.objects.get(user_id=user.id, status=False)
        except Exception:
            return False
        if token.is_alive and token.tokentype == 1:
            if token.get_vrfcode() == verf_code:
                return True
            else:
                return False
        return False

    def sendPhoneVerfText(self, user_id):
        """Sends a text to the user saying that his phone has been verified"""
        user = self.getUserDetails(user_id)
        vas = Sparrow()
        msg = "Your phone has been verified, Thankyou"
        logger.debug(msg)
        status = vas.sendMessage(msg, user)
        return status

    def sendPasswordVerfText(self, user_id):
        """Sends a text to the user with his password"""
        user = self.getUserDetails(user_id)
        token = UserToken.objects.get(user_id=user, tokentype=1, status=False)
        vas = Sparrow()
        msg = messages.SEND_PASSWD_MSG.format(token.get_vrfcode())
        logger.debug(msg)
        status = vas.sendMessage(msg, user)
        return status

    def getEBUserList(self):
        """
        Returns EB User list
        """
        ebusers = EarlyBirdUser.objects.all()
        return ebusers

    def getUserList(self, phone):
        """
        Returns list of the users in the phone
        searches via the phone number
        """
        # for users might not want to put a +977
        phone = '+977'+phone
        userlist = UserProfile.objects.filter(
            phone__startswith=phone,
            user_type='2'
        )
        return userlist


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
