from django.conf.urls import patterns, include, url

import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MentorFinder2.views.home', name='home'),
    # url(r'^MentorFinder2/', include('MentorFinder2.foo.urls')),
    url(r'^all/$',
        views.FieldList.as_view(),
        name='all_fields'),
    url(r'^detail/(?P<pk>\d+)/$',
        views.FieldDetail.as_view(),
        name='field_detail'),
    # url(r'^profile/$', views.member_profile, name='member_profile'),
    url(r'^categories/$',
        views.CategoryList.as_view(),
        name='category_list'),
)