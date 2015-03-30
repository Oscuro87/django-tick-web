from django.conf.urls import url, include
from rest_framework import routers
from restserver import views

#TODO: urls.py pour rest server (voir http://www.django-rest-framework.org/tutorial/quickstart/)

urlpatterns = [
    url(r'auth', views.RESTLogin.as_view(), name="REST-login"),
    url(r'logout', views.RESTLogout.as_view(), name="REST-logout"),
    url(r'tickets/simple', views.RESTSimpleTicketList.as_view(), name="REST-simple-tickets"),


    # Config
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]