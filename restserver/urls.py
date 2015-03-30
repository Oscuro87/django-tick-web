from django.conf.urls import url, include
from rest_framework import routers
from restserver import views

#TODO: urls.py pour rest server (voir http://www.django-rest-framework.org/tutorial/quickstart/)

urlpatterns = [
    url(r'auth', views.RESTLogin.as_view()),
    url(r'logout', views.RESTLogout.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]