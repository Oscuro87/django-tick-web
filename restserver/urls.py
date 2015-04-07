from django.conf.urls import url, include
from restserver import views

# DOC: http://www.django-rest-framework.org/tutorial/quickstart/

urlpatterns = [
    url(r'auth', views.RESTLogin.as_view(), name="REST-login"),
    url(r'logout', views.RESTLogout.as_view(), name="REST-logout"),
    url(r'tickets/simple', views.RESTSimpleTicketList.as_view(), name="REST-simple-tickets"),
    url(r'tickets/full$', views.RESTFullTicket.as_view(), name="REST-full-ticket"),
    url(r'tickets/full/comments', views.RESTFullTicketComment.as_view(), name="REST-full-ticket-comments"),
    url(r'tickets/full/history', views.RESTFullTicketHistory.as_view(), name="REST-full-ticket-histories"),
    url(r'tickets/full/createComment', views.RESTCreateTicketComment.as_view(), name="REST-full-ticket-create-comment"),

    # Config
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]