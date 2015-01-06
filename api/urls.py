from django.conf.urls import patterns, url, include

import views as apiview
import rest_framework_swagger

from rest_framework.urlpatterns import format_suffix_patterns
# from rest_framework.authtoken import views
urlpatterns = patterns('',
    # Examples:
    url(r'^api-auth/$', apiview.obtain_auth_token),
    # url(r'^signup/$', apiview.UserSignup.as_view()),
    # url(r'^users/$', apiview.UsersList.as_view()),
    url(r'^users/(?P<pk>\w+)/$', apiview.UsersDetail.as_view()),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^jobs/$', apiview.JobsDetail.as_view()),
    url(r'^jobs/(?P<pk>\w+)/$', apiview.JobDetail.as_view()),
    url(r'^verify/$', apiview.VerifyPhone.as_view(), name='verifyPhone'),
    # url(r'^getprice/$', apiview.PriceCalculator.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)
