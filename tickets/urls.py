from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', include('login.urls')),
    url(r'^login/', include('login.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/', include('ticketing.urls')),
    url(r'^rest/', include('restserver.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)
