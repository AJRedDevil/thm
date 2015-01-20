from django.conf.urls import patterns, url, include
from django.conf import settings

import views as apiview
import rest_framework_swagger

from rest_framework.urlpatterns import format_suffix_patterns
# from rest_framework.authtoken import views
urlpatterns = patterns('',
    # Examples:
    url(r'^api-auth/$', apiview.obtain_auth_token),
    url(r'^users/(?P<pk>\w+)/$', apiview.UsersDetail.as_view()),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^jobs/$', apiview.JobsDetail.as_view()),
    url(r'^jobs/(?P<pk>\w+)/$', apiview.JobDetail.as_view()),
    url(r'^verify/$', apiview.VerifyPhone.as_view(), name='verifyPhone'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
		url(r'^signup/$', apiview.UserSignup.as_view()),
		url(r'^users/$', apiview.UsersList.as_view()),
        ) 

urlpatterns = format_suffix_patterns(urlpatterns)

