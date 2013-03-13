from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MentorFinder2.views.home', name='home'),
    # url(r'^MentorFinder2/', include('MentorFinder2.foo.urls')),
    url(r'^join/$', views.join, name='join'),
    url(r'^$', views.home, name='home'),
    url(r'^profile/(?P<pk>\d+)/$', views.member_profile, name='member_profile'),
    url(r'^add_field/$', views.add_field, name='add_field'),
    url(r'^view_members/$', views.ViewMembers.as_view(), name='view_members'),
    url(r'^member_detail/(?P<pk>\d+)/$', views.member_detail, name='member_detail'),
    url(r'^delete_field/(?P<field_pk>\d+)/$', views.delete_field, name='delete_field'),
    url(r'^new_job/$', views.new_job, name='new_job')


)