from .models import SMSLog, SMSLogManager

import os
import logging
import requests

# Init Logger
logger = logging.getLogger(__name__)

class Sparrow(object):
    """
    Sparrow SMS Handler for the App
    """
    def __init__(self):
        self.__outgoingurl='https://api.sparrowsms.com/call_in.php'
        self.__clientid = os.environ['SPARROW_CLIENT_ID']
        self.__username = os.environ['SPARROW_USERNAME']
        self.__password = os.environ['SPARROW_PASSWORD']

    def setparams(self, message, user):
        params = dict(
            client_id = self.__clientid,
            username = self.__username,
            password = self.__password,
            to = str(user.phone.as_international),
            text = message
            )
        return params

    def sendMessage(self, message, user):
        getparams = self.setparams(message, user)
        try:
            req = requests.post(self.__outgoingurl, getparams, verify=False)
            if req.status_code == 200:
                logger.warn(message)
                sm = SMSLogManager()
                sm.updateLog(user, message)
                return req.content
            else:
                logger.warn("Error sending SMS to {0}".format(
                    user.phone.as_international))
                return req.content
        except Exception, e:
            logger.warn("Error sending SMS to {0}".format(
                user.phone.as_international))
            logger.warn("Error : {0}".format(e))
            # Because the request doesn't turn out well, we just pass it
            return e


    def sendDirectMessage(self, message, phone):
        logger.warn(message)
        params = dict(
            client_id = self.__clientid,
            username = self.__username,
            password = self.__password,
            to = phone.as_international,
            text = message
            )
        try:
            req = requests.post(self.__outgoingurl, params, verify=False)
            resp = req.content
            return resp
        except Exception, e:
            logger.warn("Error sending SMS to {0}".format(
                phone.as_international))
            logger.warn("Error : {0}".format(e))
            # Because the request doesn't turn out well, we just pass it
            return e
