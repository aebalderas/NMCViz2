#NMCharts/Charts
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django import forms
from views import *

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = patterns('',
    url(r'^$', hellocharts, name='charts'),

    url(r'^odtimesinfo/$', odTimesInfo, name='odtimesinfo'),
    url(r'^distanceinfo/$', distanceInfo, name='distanceinfo'),
    url(r'^turnmoveinfo/$', turnMoveInfo, name='turnmoveinfo'),
    url(r'^traveltimeinfo/$', travelTimeInfo, name='traveltimeinfo'),
    url(r'^volumeinfo/$', volumeCountsInfo, name='volumeinfo'),

    url(r'^predistance/$', preDistance, name='predistance'),
    url(r'^loaddistance/(?P<network>.+)/(?P<host>.+)/(?P<pwd>.+)/(?P<user>.+)/(?P<route>.+)$', loaddistance),

    url(r'^preodtimes/$', preODTimes, name='preodtimes'),
    url(r'^loadodtimes/(?P<network>.+)/(?P<host>.+)/(?P<pwd>.+)/(?P<user>.+)/(?P<origins>.+)/(?P<destinations>.+)$', loadodtimes),

    url(r'^pretraveltime/$', preTravelTime, name='pretraveltime'),
    url(r'^loadtraveltime/(?P<network>.+)/(?P<host>.+)/(?P<pwd>.+)/(?P<user>.+)/(?P<start>.+)/(?P<end>.+)$', loadtraveltime),

    url(r'^preturnmove/$', preTurnMove, name='preturnmove'),
    url(r'^loadturnmove/(?P<network>.+)/(?P<host>.+)/(?P<pwd>.+)/(?P<user>.+)/(?P<links>.+)$', loadturnmove),

    url(r'^prevolume/$', preVolume, name='prevolume'),
    url(r'^loadvolume/(?P<network>.+)/(?P<host>.+)/(?P<pwd>.+)/(?P<user>.+)/(?P<links>.+)/(?P<start>.+)/(?P<end>.+)$', loadvolume),
)
urlpatterns += staticfiles_urlpatterns()
