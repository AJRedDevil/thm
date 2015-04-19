from django.conf import settings
from django.conf.urls import patterns, include, url
# from django.contrib import admin
# admin.autodiscover()

from pricing import views as pricingView

urlpatterns = patterns('',
    url(r'^$', pricingView.viewPricing, name='viewPricing'),
)
