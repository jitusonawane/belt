from django.conf.urls import url
from django.contrib import admin
from . import views  


urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),      
    url(r'^travel$', views.travel),
    url(r'^add_trip/$', views.add_trip),
    url(r'^your_trip/$', views.your_trip),
    url(r'^detail/(?P<id>\d+)?$', views.detail),
    url(r'^join_trip/(?P<id>\d+)$', views.join_trip),
    
]