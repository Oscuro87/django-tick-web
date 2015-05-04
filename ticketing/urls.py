from django.conf.urls import patterns, url
from ticketing import views

urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view(), {}, 'homeview'),
    url(r'^$', views.HomeView.as_view(), {}, 'assigntickettome'),
    url(r'^ticket/detail/(?P<ticket_id>\d[0-9]*)/$', views.TicketView.as_view(), {}, 'ticketdetailview'),
    url(r'^contact/$', views.ContactView.as_view(), {}, 'contactview'),
    url(r'^create/ticket/$', views.CreateTicketView.as_view(), {}, 'createticketview'),
    url(r'^create/location/$', views.CreateLocationView.as_view(), {}, 'createlocationview'),
    url(r'^account/entreprise/update/$', views.UpdateCompanyView.as_view(), {}, 'updatecompanyinfos'),
    url(r'^account/building/update/$', views.UpdateBuildingView.as_view(), {}, 'updatebuildingview'),
)