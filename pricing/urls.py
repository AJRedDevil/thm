from django.conf.urls import patterns, url

from pricing import views as pricingView

urlpatterns = patterns(
    '',
    url(r'^$', pricingView.viewPricing, name='viewPricing'),
)
