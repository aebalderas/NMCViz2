#nmc/mainurls

from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^network/', include('network.urls', namespace="network"), name='network'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', hello, name='hello'),
    url(r'^charts/', include('Charts.urls')),
    
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
urlpatterns += staticfiles_urlpatterns()
