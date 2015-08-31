

from django.conf.urls import patterns, url

from apps.subscription import views as subscriptionView

urlpatterns = patterns(
	'',
	url(r'^$', subscriptionView.viewSubscription, name="subscriptions"),
	url(r'^viewsubscription/(?P<subscription_id>[\w\d]+)/$', subscriptionView.viewSubscription, name="subscription"),
	url(r'^createsubscription/$', subscriptionView.createSubscription, name='createSubscription'),
	url(r'^editsubscription/(?P<subscription_id>[\w\d]+)/$', subscriptionView.editSubscription, name='editSubscription'),
	url(r'^createsubscriptionpackage/$', subscriptionView.createSubscriptionPackage, name="createSubscriptionPackage"),
	url(r'^viewsubscriptionpackage/$', subscriptionView.viewSubscriptionPackage, name="viewSubscriptionPackages"),
	url(r'^viewsubscriptionpackage/(?P<subscription_pkg_id>[\w\d]+)/$', subscriptionView.viewSubscriptionPackage, name="viewSubscriptionPackage"),
	url(r'^editsubscriptionpackage/(?P<subscription_pkg_id>[\w\d]+)/$', subscriptionView.editSubscriptionPackage, name="editSubscriptionPackage"),
	url(r'^createsubscriber/$', subscriptionView.createSubscriber, name="createSubscriber"),
	url(r'^editsubscriber/(?P<subscriber_id>[\w\d]+)/$', subscriptionView.editSubscriber, name="editSubscriber"),
	url(r'^viewsubscriber/$', subscriptionView.viewSubscriber, name="subscribers"),
	url(r'^viewsubscriber/(?P<subscriber_id>[\w\d]+)/$', subscriptionView.viewSubscriber, name="subscriber"),
)