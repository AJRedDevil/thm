

import datetime
import logging
import pytz
from django.core import serializers
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import SubscriptionPackage, Subscriber, Subscription
from apps.jobs.models import Jobs

logger = logging.getLogger(__name__)

class SubscriptionManager(object):
    """Manager to handle subscription model
    """
    def getSubscriptionPackageList(self,) :
        """List all the subscription package
        """
        subscription_pkgs = SubscriptionPackage.objects.all()
        return subscription_pkgs

    def getSubscriptionPackageDetail(self, pkg_id):
        """Return the detail of required subscription package
        """
        subscription_pkg = get_object_or_404(SubscriptionPackage, id=pkg_id)
        return subscription_pkg

    def getSubscriberList(self):
        """Return the subscriber list
        """
        subscribers = Subscriber.objects.all().order_by('id')
        return subscribers

    def getSubscriberDetail(self, subscriber_id):
        """Return the detail of required subscriber
        """
        subscriber = get_object_or_404(Subscriber, id=subscriber_id)
        return subscriber

    def getSubscriptionList(self, terminated=False):
        """Return the subscription list
        """
        if terminated:
            subscriptions = Subscription.objects.filter(terminated=terminated)
        else:   
            subscriptions = Subscription.objects.filter(terminated=terminated)
        return subscriptions

    def __convert_naive_to_aware(self, _date):
        return datetime.datetime.combine(_date,datetime.time(0,0))

    def __get_localize(self, _date):
        return pytz.timezone("Asia/Kathmandu").localize(_date, is_dst=None)

    def __getRemainingRepair(self, subscriber_id):
        """Returns the remainig repair of the subscriber
        """
        current_date = timezone.now().date()
        remaining_repair = 0
        
        subscriber = get_object_or_404(Subscriber, id=subscriber_id)
        subscription = Subscription.objects.filter(subscriber=subscriber, terminated=False)
        
        if subscription:
            subscription = subscription[0]
            subscription_pkg = subscription.package
            max_repair = subscription_pkg.max_repair

            start_date = subscription.start_date
            end_date = subscription.end_date

            total_days = end_date - start_date
            
            gone_days = current_date - start_date
            number_of_months = total_days / 30
            number_of_months_gone = int(gone_days.days/30)

            if gone_days.days > 0:
                month_starting_date = start_date + datetime.timedelta(days=(number_of_months_gone*30))
            else:
                month_starting_date = start_date
            remaining_days = (end_date - current_date).days
            if month_starting_date < end_date:
                if remaining_days >=30:
                    month_ending_date = month_starting_date + datetime.timedelta(days=30)
                    month_starting_date = self.__convert_naive_to_aware(month_starting_date)
                    month_ending_date = self.__convert_naive_to_aware(month_ending_date)
                    a=self.__get_localize(month_starting_date)
                    b=self.__get_localize(month_ending_date)
                    all_jobs_completed_count = Jobs.objects.filter(completion_date__range=[a, b], customer=subscriber).count()
                    remaining_repair = max_repair - all_jobs_completed_count
                elif remaining_days < 30:
                    month_ending_date = start_date + datetime.timedelta(days=(30+remaining_days))
                    month_starting_date = self.__convert_naive_to_aware(month_starting_date)
                    month_ending_date = self.__convert_naive_to_aware(month_ending_date)    
                    a=self.__get_localize(month_starting_date)
                    b=self.__get_localize(month_ending_date)
                    all_jobs_completed_count = Jobs.objects.filter(completion_date__range=[a, b], customer=subscriber).count()
                    remaining_repair = max_repair - all_jobs_completed_count

        return remaining_repair

    def getRemainingRepairs(self, subscriber_id=None):
        # what about certain range?
        # what about completed repairs count
        if subscriber_id:
            return {str(subscriber_id):self.__getRemainingRepair(subscriber_id)}
        else:
            all_remaining_repairs = {}
            subscribers = self.getSubscriberList()
            for subscriber in subscribers:
                all_remaining_repairs.update({str(subscriber.id):self.__getRemainingRepair(subscriber_id=subscriber.id)})
            return all_remaining_repairs

    def getCompletedRepairsCount(self, starting_date, subscriber):
        ending_date = datetime.date.today()
        return Jobs.objects.filter(completion_date__range=[starting_date, ending_date], customer=subscriber).count()

    def getSubscriptionDetail(self, subscription_id):
        """Return the subscription detail
        """
        subscription = get_object_or_404(Subscription, id=subscription_id)
        return subscription

