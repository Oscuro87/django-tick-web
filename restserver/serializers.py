from django_countries.fields import CountryField
from login.models import TicketsUser
from rest_framework import serializers
from ticketing.models import Ticket, TicketStatus, Building, Channel, EventCategory, TicketPriority, Company, \
    TicketComment, TicketHistory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketsUser
        fields = ('pk', 'first_name', 'last_name', 'email', 'is_active', 'is_staff')


class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketStatus
        fields = ('pk', 'label',)


class SimpleTicketSerializer(serializers.ModelSerializer):
    fk_reporter = UserSerializer(many=False, read_only=True)
    fk_manager = UserSerializer(many=False, read_only=True)
    fk_status = TicketStatusSerializer(many=False, read_only=True)

    class Meta:
        model = Ticket
        fields = ('pk', 'ticket_code', 'fk_reporter', 'fk_manager', 'fk_status')


class BuildingSerializer(serializers.ModelSerializer):
    #country = CountryField()

    class Meta:
        model = Building
        fields = (
            'country',
            'address',
            'vicinity',
            'postcode',
            'building_name',
            'building_code',
        )


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = (
            'label',
        )


class TicketPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketPriority
        fields = (
            'label',
        )


class CategorySerializer(serializers.ModelSerializer):
    fk_priority = TicketPrioritySerializer(many=False, read_only=True)

    class Meta:
        model = EventCategory
        fields = (
            'fk_parent_category',
            'fk_priority',
            'label',
        )
        depth = 1

class CompanySerializer(serializers.ModelSerializer):
    fk_suitableEventCategories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = (
            'fk_suitableEventCategories',
            'country',
            'address',
            'vicinity',
            'postcode',
            'phone_number',
            'name',
            'vat_number',
        )


class FullTicketSerializer(serializers.ModelSerializer):
    fk_building = BuildingSerializer(many=False, read_only=True)
    fk_channel = ChannelSerializer(many=False, read_only=True)
    fk_category = CategorySerializer(many=False, read_only=True)
    fk_reporter = UserSerializer(many=False, read_only=True)
    fk_priority = TicketPrioritySerializer(many=False, read_only=True)
    fk_status = TicketStatusSerializer(many=False, read_only= True)
    fk_manager = UserSerializer(many=False, read_only=True)
    fk_company = CompanySerializer(many=False, read_only=True)

    class Meta:
        model = Ticket
        fields = (
            'fk_building',
            'fk_channel',
            'fk_category',
            'fk_reporter',
            'fk_priority',
            'fk_status',
            'fk_manager',
            'fk_company',
            'ticket_code',
            'floor',
            'office',
            'intervention_date',
            'description',
        )


class TicketCommentSerializer(serializers.ModelSerializer):
    fk_ticket = FullTicketSerializer(many=False, read_only=True)
    fk_commenter = UserSerializer(many=False, read_only=True)

    class Meta:
        model = TicketComment
        fields = (
            'fk_ticket',
            'fk_commenter',
            'date_created',
            'comment',
        )


class TicketHistorySerializer(serializers.ModelSerializer):
    fk_ticket = FullTicketSerializer(many=False, read_only=True)
    fk_ticket_status = TicketStatusSerializer(many=False, read_only=True)
    fk_manager = UserSerializer(many=False, read_only=True)

    class Meta:
        model = TicketHistory
        fields = (
            'fk_ticket',
            'fk_ticket_status',
            'fk_manager',
            'update_date',
            'update_reason',
        )