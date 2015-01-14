from django import template

from ticketing.models import EventCategory, Building, Place
from login.models import TicketsUser

register = template.Library()

@register.filter(name="get_all_parent_categories")
def get_all_parent_categories(retVal):
    retVal = EventCategory.objects.filter(fk_parent_category__exact=None)
    return retVal

@register.filter(name="get_all_buildings_for_user")
def get_all_buildings_for_user(user_pk):
    try:
        user = TicketsUser.objects.get(pk=user_pk)
        assert isinstance(user, TicketsUser)
        pre_selection = Place.objects.filter(fk_renter__exact=user.pk)
        selection = []
        for p in pre_selection:
            assert isinstance(p, Place)
            temp = {'pk': p.fk_building.pk, 'building_name': p.fk_building.building_name}
            selection.append(temp)
        return selection
    except AssertionError:
        pass

    return []

@register.filter(name="count_entries")
def count_entries(table):
    return len(table)