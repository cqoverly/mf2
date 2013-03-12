from django.conf.urls import patterns, include, url


import views

urlpatterns = patterns('',
    url(r'^request/(?P<mentor_pk>\d+)$',
        views.request_mentorship,
        name='request_mentorship'),
    url(r'^accept/(?P<pk>\d+)$',
        views.accept_mentorship,
        name='accept_mentorship'),
    )