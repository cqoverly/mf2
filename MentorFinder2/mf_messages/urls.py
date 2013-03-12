from django.conf.urls import patterns, include, url

import views


urlpatterns = patterns('',
    url(r'^new/(?P<member_id>\w+)/$', views.new_message, name='new_message'),
    )