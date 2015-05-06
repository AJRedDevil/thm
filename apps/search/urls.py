from django.conf.urls import patterns, url
import apps.search.views as searchviews

urlpatterns = patterns(
    '',
    url(r'^$', searchviews.userSearch, name='userSearch'),
    url(r'user/$', searchviews.userSearchDetail, name='userSearchDetail'),
)
