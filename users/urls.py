from django.conf import settings
from django.conf.urls import patterns, include, url
# from django.contrib import admin
# admin.autodiscover()

from users import views as userviews

urlpatterns = patterns('',
    url(r'(?P<userref>\w+)/$', userviews.editUserDetail, name='editUserDetail' ),
)
