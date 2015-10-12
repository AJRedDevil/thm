
from django.conf.urls import patterns, include, url
# from django.contrib import admin
# admin.autodiscover()

from apps.jobs import views as jobviews

urlpatterns = patterns('',
    url(r'^calendar/events/$', jobviews.events, name='jobCalendarEvents'),
    url(r'^calendar/$', jobviews.calendar, name='jobCalendar'),
    url(r'^scheduler/update/(?P<job_scheduler_id>[\w\d]+)/$', jobviews.updateJobScheduler, name='updateJobScheduler'),
    url(r'^scheduler/(?P<job_scheduler_id>[\w\d]+)/$', jobviews.viewJobScheduler, name='jobScheduler'),
    url(r'(?P<job_id>\w+)/$', jobviews.viewJob, name='viewJob'),

)
