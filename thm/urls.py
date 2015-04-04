from django.conf import settings
from django.conf.urls import patterns, include, url
# from django.contrib import admin
# admin.autodiscover()

from users import views as userviews
from jobs import views as jobviews
from .views import index
import logging

urlpatterns = patterns(
    '',
    url(r'^signin/$', userviews.signin, name='signin'),
    url(r'^logout/$', userviews.logout, name='logout'),
    url(r'^home/$', userviews.home, name='home'),
    url(r'^createhandymen/$', userviews.createhandymen, name='createhandymen'),
    url(r'^createuser/', userviews.createUser, name='createUser'),
    url(r'^newuser/$', userviews.viewEBUser, name='viewEBUser'),
    url(r'^createjob/$', jobviews.createJob, name='createJob'),
    url(r'^register/$', userviews.joinasuser, name='register'),
    url(r'^e48kucfb5pq/$', userviews.smsEndpoint, name='smsEndpoint'),
    url(r'^4DEa6cvdaP0/$', userviews.gaTracker, name='gaTracker'),
    url(r'^verify/$', userviews.verifyPhone, name='verifyPhone'),
    url(r'^sendvrfcode/$', userviews.sendVrfCode, name='sendVrfCode'),
    url(r'^settings/$', userviews.userSettings, name='userSettings'),
    url(r'^settings/changepassword/$', userviews.changePassword, name='changePassword'),
    url(r'^resetpassword/', userviews.resetPasswordToken, name='resetPasswordToken'),
    url(r'^forgetpassword/$', userviews.sendPasswdVrfCode, name='sendPasswdVrfCode'),
    url(r'^search/', include('search.urls')),
    url(r'^faq/', include('faq.urls')),
    url(r'^jobs/', include('jobs.urls')),
    url(r'^work/', include('job_gallery.urls')),
    url(r'^$', index, name='index'),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^api/v1/', include('api.urls')),
        url(r'^signup/$', userviews.signup, name='signup'),
        url(r'^profile/$', userviews.myProfile, name='myProfile'),
    )

urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
