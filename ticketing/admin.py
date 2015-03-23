from django.contrib import admin

from ticketing.models import Building, Channel, EventCategory, Company, TicketHistory, Place, \
    TicketPriority, TicketStatus, Ticket, TicketComment
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
admin.site.register(TicketComment)
admin.site.register(Place)
admin.site.register(TicketPriority)
admin.site.register(TicketStatus)
admin.site.register(Ticket, TicketAdmin)
