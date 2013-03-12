from django.conf.urls import patterns, include, url

import views


urlpatterns = patterns('',
    url(r'^new/(?P<member_id>\d+)/$', views.new_message, name='new_message'),
    url(r'^msg_list/$', views.MFMessage_list.as_view(), name='mfmessage_list'),
    url(r'^msg_detail/(?P<msg_id>\d+)/$', views.mfmessage_detail, name='mfmessage_detail'),
    )