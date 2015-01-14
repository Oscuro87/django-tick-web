from django.contrib import admin
from django import forms
from django.forms.utils import ErrorList
from ticketing.models import Building, Channel, EventCategory, Company, TicketHistory, Place, \
    TicketPriority, TicketStatus, Ticket, CompanyManager
from login.models import TicketsUser, TicketsUserManager


class TicketAdminForm(forms.ModelForm):
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, instance=None):
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance)
        tum = TicketsUserManager()
        compMan = CompanyManager()
        self.fields['fk_manager'].queryset = tum.get_managers_only()
        self.fields['fk_renter'].queryset = tum.get_renters_for_building_id(None)
        self.fields['fk_company'].queryset = compMan.get_companies_for_event_category(self.fields['fk_category'].queryset.last())


class TicketAdmin(admin.ModelAdmin):
    readonly_fields = ['ticket_code',]
    form = TicketAdminForm

    # def get_queryset(self, **kwargs):
    #     qs = self.model.objects.get_queryset(kwargs)
    #     ordering = self.ordering or ()
    #     if ordering:
    #         qs = qs.order_by(*ordering)
    #     return qs


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
