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
    url(r'^logout/$', userviews.logout, name='logout'),
    url(r'^home/$', userviews.home, name='home'),
    url(r'^createhandymen/$', userviews.createhandymen, name='createhandymen'),
    url(r'^$', index, name='index'),
)
