from django.conf.urls import patterns, url
from ticketing import views

urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view(), {}, 'homeview'),
    url(r'^$', views.HomeView.as_view(), {}, 'assigntickettome'),
    url(r'^ticket/detail/(?P<ticket_id>\d[0-9]*)/$', views.TicketView.as_view(), {}, 'ticketdetailview'),
    url(r'^contact/$', views.ContactView.as_view(), {}, 'contactview'),
    url(r'^create/ticket/$', views.CreateTicketView.as_view(), {}, 'createticketview'),
)