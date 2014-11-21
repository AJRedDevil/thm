from django.conf.urls import patterns, url

import views as apiview

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views
urlpatterns = patterns('',
    # Examples:
    url(r'^api-auth/$', views.obtain_auth_token),
    url(r'^users/$', apiview.UsersList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', apiview.UsersDetail.as_view()),
    # url(r'^quests/$', apiview.QuestsList.as_view()),
    # url(r'^quests/(?P<pk>[0-9]+)/$', apiview.QuestsDetail.as_view()),
    # url(r'^getprice/$', apiview.PriceCalculator.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)
