from django.conf.urls import url, include
from rest_framework import routers
from restserver import views

#TODO: urls.py pour rest server (voir http://www.django-rest-framework.org/tutorial/quickstart/)

urlpatterns = [
    url(r'auth', views.rest_login),
    url(r'logout', views.rest_logout),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]