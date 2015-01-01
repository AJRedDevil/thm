from django.conf import settings
from django.conf.urls import patterns, include, url
# from django.contrib import admin
# admin.autodiscover()

from users import views as userviews
from .views import index

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'thm.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include('api.urls') ),
    url(r'^signin/$', userviews.signin, name='signin'),
    url(r'^signup/$', userviews.signup, name='signup'),
    url(r'^logout/$', userviews.logout, name='logout'),
    url(r'^home/$', userviews.home, name='home'),
    url(r'^createhandymen/$', userviews.createhandymen, name='createhandymen'),
    url(r'^createuser/$', userviews.createUser, name='createUser'),
    url(r'^register/$', userviews.joinasuser, name='register'),
    url(r'^joinus/$', userviews.joinashandymen, name='joinus'),
    url(r'^verify/$', userviews.verifyPhone, name='verifyPhone'),
    url(r'^sendvrfcode/$', userviews.sendVrfCode, name='sendVrfCode'),
    url(r'^myprofile/$', userviews.myProfile, name='myProfile'),
    url(r'^$', index, name='index'),
)

urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )