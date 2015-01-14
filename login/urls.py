from django.conf.urls import patterns, url
from login import views

urlpatterns = patterns('',
    url(r'^$', views.LoginView.as_view(), {}, 'loginview'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',  {'next_page': 'loginview'}, 'logout'),
)
