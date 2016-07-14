from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'WordlBank.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'WB.views.home', name='home'),
    url(r'^upload/$', 'WB.views.upload', name='upload'),
    url(r'^main/$', 'WB.views.main', name='main'),
    url(r'^rest_pbsb/$', 'WB.views.rest_pbsb', name='rest_pbsb'),
    url(r'^rest_categories/$', 'WB.views.rest_categories', name='rest_categories'),
    url(r'^view_list/$', 'WB.views.view_list', name='view_list'),
    url(r'^save/$', 'WB.views.save', name='save'),
    url(r'^remove_query/$', 'WB.views.remove_query', name='remove_query'),
    url(r'^download_query/(?P<id_q>\w+)$', 'WB.views.download_query', name='download_query'),
    url(r'^download_indicators/$', 'WB.views.download_indicators', name='download_indicators'),

    url(r'^admin/', include(admin.site.urls)),
)
