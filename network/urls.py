from django.conf.urls import patterns, url

from network import views

urlpatterns = patterns('',
    url(r'^new/$', views.new_network, name='new'),
    url(r'^new/error/(?P<errormsg>.+)/', views.network_error, name='error'),
    url(r'^new/ok/', views.network_ok, name='ok'),
    url(r'^visualize/(?P<name>.+)/', views.visualize),
    url(r'^load_data/(?P<network_name>.+)/(?P<start>.+)/(?P<interval>.+)/(?P<terminate>.+)$', views.load_data),
    url(r'^$', views.network),
)   