from django.conf.urls import patterns, url

from apps.commcalc import views as commissionView

urlpatterns = patterns(
    '',
    url(r'^$', commissionView.viewCommission, name='viewCommission'),
)
