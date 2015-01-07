from django.conf import settings
from django.conf.urls import patterns, include, url
# from django.contrib import admin
# admin.autodiscover()

from jobs import views as jobviews

urlpatterns = patterns('',
    url(r'(?P<job_id>\w+)/$', jobviews.viewJob, name='viewJob' ),
)
