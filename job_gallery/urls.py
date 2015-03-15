from django.conf import settings
from django.conf.urls import patterns, include, url
# from django.contrib import admin
# admin.autodiscover()

import job_gallery.views as jgviews

urlpatterns = patterns(
    '',
    url(r'upload/(?P<job_id>[\w\d]+)/$', jgviews.uploadJobPhotos, name='uploadJobPhotos'),
)
