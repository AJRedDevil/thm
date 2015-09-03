

import logging
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import SubscriptionCreationForm, SubscriptionEditForm, SubscriberCreationForm, SubscriberEditForm, SubscriptionPackageCreationForm, SubscriptionPackageEditForm
from .handler import SubscriptionManager
from apps.users.models import UserProfile
from thm.decorators import is_superuser

logger = logging.getLogger(__name__)

# Create your views here.

### Subscription
@login_required
@is_superuser
def createSubscription(request):
    """Handles the creation of Subscription request
    """
    user = request.user
    sm = SubscriptionManager()
    if request.method == 'GET':
        subscription_form = SubscriptionCreationForm()
        return render(request, 'createSubscription.html', locals())
    elif request.method == 'POST':
        subscription_form = SubscriptionCreationForm(request.POST)
        if subscription_form.is_valid():
            subscription_form.save()
            return redirect('subscriptions')
        if subscription_form.errors:
            logging.warn("Form has errors, %s", subscription_form.errors)
        return render(request, 'createSubscription.html', locals())

@login_required
@is_superuser
def editSubscription(request, subscription_id=None):
    """Handles the request for editing Subscrition changes
    """
    sm = SubscriptionManager()
    subscription = sm.getSubscriptionDetail(subscription_id)
    subscription_form = SubscriptionEditForm(request.POST, instance=subscription)
    if subscription_form.is_valid():
        subscription_form.save()
        return redirect('subscriptions')
    if subscription_form.errors:
        logging.warn("Form has errors, %s", subscription_form.errors)
        return render(request, 'editSubscription.html', locals())

@login_required
@is_superuser
def viewSubscription(request, subscription_id=None):
    """Handles the listing or detail view of Subscription
    """
    user = request.user
    sm = SubscriptionManager()
    if subscription_id:
        subscription = sm.getSubscriptionDetail(subscription_id)
        subscription_form = SubscriptionEditForm(instance=subscription)
        remaining_repairs = sm.getRemainingRepairs(subscription.subscriber.id)
        remaining_repairs = remaining_repairs[str(subscription.subscriber.id)]
        return render(request, 'editSubscription.html', locals())
    else:
        subscriptions = sm.getSubscriptionList()
        remaining_repairs = sm.getRemainingRepairs()
        for subscription in subscriptions:
            subscriber_id = str(subscription.subscriber.id)
            if subscriber_id in remaining_repairs.keys():
                subscription.remaining_repairs = remaining_repairs[str(subscription.subscriber.id)]
        return render(request, 'subscription.html', locals())


### Subscription Package
@login_required
@is_superuser
def createSubscriptionPackage(request):
    """Handles the creation of SubscriptionPackage request
    """
    user = request.user
    sm = SubscriptionManager()
    if request.method == 'GET':
        subscription_pkg_form = SubscriptionPackageCreationForm()
        return render(request, 'createSubscriptionPackage.html', locals())
    elif request.method == 'POST':
        subscription_pkg_form = SubscriptionPackageCreationForm(request.POST)
        if subscription_pkg_form.is_valid():
            subscription_pkg_form.save()
            return redirect('viewSubscriptionPackages')
        if subscription_pkg_form.errors:
            logging.warn("Form has errors, %s", subscription_pkg_form.errors)
        return render(request, 'createSubscriptionPackage.html', locals())

@login_required
@is_superuser
def editSubscriptionPackage(request, subscription_pkg_id):
    """Handles the request for editing SubscriptionPackage changes
    """
    user = request.user
    sm = SubscriptionManager()
    subscription_pkg = sm.getSubscriptionPackageDetail(subscription_pkg_id)
    subscription_pkg_form = SubscriptionPackageEditForm(request.POST, instance=subscription_pkg)
    if subscription_pkg_form.is_valid():
        subscription_pkg_form.save()
        return redirect('viewSubscriptionPackages')
    if subscription_pkg_form.errors:
        logging.warn("Form has errors, %s", subscription_pkg_form.errors)
        return render(request, 'editSubscriptionPackage.html', locals())

@login_required
@is_superuser
def viewSubscriptionPackage(request, subscription_pkg_id=None):
    """Handles the listing or detail view of SubscriptionPackage
    """
    user = request.user
    sm = SubscriptionManager()
    if subscription_pkg_id:
        subscription_pkg = sm.getSubscriptionPackageDetail(subscription_pkg_id)
        subscription_pkg_form = SubscriptionPackageEditForm(instance=subscription_pkg)
        return render(request, 'editSubscriptionPackage.html', locals())
    else:
        subscription_pkgs = sm.getSubscriptionPackageList()
        return render(request, 'subscriptionPackage.html', locals())


### Subscriber
@login_required
@is_superuser
def createSubscriber(request):
    """Handles the creation of Subscriber request
    """
    user = request.user
    sm = SubscriptionManager()
    if request.method == 'GET':
        subscriber_form = SubscriberCreationForm()
        return render(request, 'createSubscriber.html', locals())
    elif request.method == 'POST':
        subscriber_form = SubscriberCreationForm(request.POST)
        if subscriber_form.is_valid():
            subscribers=sm.getSubscriberList()
            last_id=subscribers[len(subscribers)-1].id
            subscriber=subscriber_form.save(commit=False)
            subscriber.id=last_id+1
            subscriber.save()
            return redirect('subscribers')
        if subscriber_form.errors:
            logging.warn("Form has errors, %s", subscriber_form.errors)
        return render(request, 'createSubscriber.html', locals())

@login_required
@is_superuser
def editSubscriber(request, subscriber_id):
    """Handles the request for editing Subscriber changes
    """
    user = request.user
    sm = SubscriptionManager()
    subscriber = sm.getSubscriberDetail(subscriber_id)
    subscriber_form = SubscriberEditForm(request.POST, instance=subscriber)
    if subscriber_form.is_valid():
        subscriber_form.save()
        return redirect('subscribers')
    if subscriber_form.errors:
        logging.warn("Form has errors, %s", subscriber_form.errors)
        return render(request, 'editSubscriber.html', locals())

@login_required
@is_superuser
def viewSubscriber(request, subscriber_id=None):
    """Handles the listing or detail view of Subscriber
    """
    user = request.user
    sm = SubscriptionManager()
    if subscriber_id:
        subscriber = sm.getSubscriberDetail(subscriber_id)
        subscriber_form = SubscriberEditForm(instance=subscriber)
        return render(request, 'editSubscriber.html', locals())
    else:
        subscribers = sm.getSubscriberList()
        return render(request, 'subscriber.html', locals())


