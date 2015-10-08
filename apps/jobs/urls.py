
from django.conf.urls import patterns, include, url
# from django.contrib import admin
# admin.autodiscover()

from apps.jobs import views as jobviews

urlpatterns = patterns('',
    url(r'^calendar/events/$', jobviews.events, name='jobCalendarEvents'),
    url(r'^calendar/$', jobviews.calendar, name='jobCalendar'),
    url(r'(?P<job_id>\w+)/$', jobviews.viewJob, name='viewJob'),
)
