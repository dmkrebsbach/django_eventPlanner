from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^newShow$', views.newShow),
    url(r'^createEvent$', views.createEvent),
    url(r'^shows/(?P<eventId>\d+)$', views.viewEvent),
    url(r'^shows/(?P<eventId>\d+)/join$', views.joinEvent),
    url(r'^shows/(?P<eventId>\d+)/leave$', views.leaveEvent),
    url(r'^shows/(?P<eventId>\d+)/cancel$', views.cancelEvent),       

]