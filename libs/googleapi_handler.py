"""
All google services listed here
"""
from django.conf import settings
import os
import urllib
import logging
import simplejson as json

class GeoCoding(object):
    def __init__(self):
        self.__BASEURL="https://maps.googleapis.com/maps/api/geocode/json?"
        serverkey = getattr(settings, 'GOOOGLE_API_KEY', None)
        self.__geocode_args = {'key':serverkey}
        self.__result = {}
        self.__status = False

    def __setparams(self,address):
        """
        Set address parameters
        """
        self.__geocode_args.update(address)

    def get_lat_long(self, address):
        """
        returns a dictionary with lat and long 
        """
        self.__setparams(dict(address=address['streetaddress']+','+address['city']+', Nepal'))
        url = self.__BASEURL + urllib.urlencode(self.__geocode_args)
        try:
            self.__result = json.load(urllib.urlopen(url))
        except Exception, e:
            logging.warn(e)
            print 'Error'

        if self.__result:
            self.__status = True if self.__result['status'] == 'OK' else False
        else:
            print 'Error'

        # Return only the lat long field as that's what we are concerned about
        if self.__status:
            return self.__result['results'][0]['geometry']['location']
        else:
            print 'Error'

