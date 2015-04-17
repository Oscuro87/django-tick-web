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
    url(r'tickets/createbuilding', views.RESTCreateBuilding.as_view(), name="REST-create-building"),
    url(r'tickets/getallcategories', views.RESTQueryCategories.as_view(), name="REST-query-all-categories"),
    url(r'tickets/getallbuildingsforuser', views.RESTQueryAllBuildings.as_view(), name="REST-query-all-buildigns-for-user"),
    url(r'tickets/createticket', views.RESTCreateTicket.as_view(), name="REST-create-ticket"),
    url(r'tickets/updatedetails$', views.RESTUpdateDetails.as_view(), name="REST-update-ticket-details"),
    url(r'tickets/updatedetails/nextprogression', views.RESTUpdateTicketProgression.as_view(), name="REST-update-ticket-progression"),
    url(r'tickets/updatedetails/getlistofcompanies', views.RESTGetListOfCompanies.as_view(), name="REST-get-list-of-companies"),
    url(r'tickets/updatedetails/updateticketcompany', views.RESTUpdateTicketCompany.as_view(), name="REST-update-ticket-company"),

    # Config
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]