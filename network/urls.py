from django.conf.urls import patterns, url

from network import views

urlpatterns = patterns('',
    url(r'^new/$', views.new_network, name='new'),
    url(r'^new/error/(?P<errormsg>.+)/', views.network_error, name='error'),
    url(r'^new/ok/', views.network_ok, name='ok'),
    url(r'^visualize/(?P<database>.+)/', views.visualize),
    url(r'^load_network/(?P<database>.+)/', views.load_network),
    url(r'^load_link_data/(?P<database>.+)/(?P<dataset>.+)$', views.load_link_data),
    url(r'^load_path_data/(?P<network>.+)/(?P<dataset>.+)$', views.load_path_data),
    url(r'^load_origins/(?P<network>.+)/(?P<dataset>.+)$', views.load_origins),
    url(r'^load_destinations/(?P<network>.+)/(?P<dataset>.+)/(?P<origin>.+)$', views.load_destinations),
    url(r'^load_paths/(?P<network>.+)/(?P<dataset>.+)/(?P<interval>.+)/(?P<origin>.+)/(?P<destination>.+)$', views.load_paths),
    url(r'^$', views.network),
)   