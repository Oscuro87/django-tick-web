from django.contrib import admin
from django import forms
from django.forms.utils import ErrorList

from ticketing.models import Building, Channel, EventCategory, Company, TicketHistory, Place, \
    TicketPriority, TicketStatus, Ticket
from login.models import TicketsUserManager
from ticketing.forms import TicketAdminForm


class TicketAdmin(admin.ModelAdmin):
    readonly_fields = ['ticket_code', ]
    form = TicketAdminForm


class EventCategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Building)
admin.site.register(Channel)
admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register(Company)
admin.site.register(TicketHistory)
admin.site.register(Place)
admin.site.register(TicketPriority)
admin.site.register(TicketStatus)
admin.site.register(Ticket, TicketAdmin)
