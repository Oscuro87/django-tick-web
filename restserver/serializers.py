from login.models import TicketsUser
from rest_framework import serializers
from ticketing.models import Ticket, TicketStatus, Building, Channel, EventCategory, TicketPriority, Company, \
    TicketComment, TicketHistory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketsUser
        fields = ('pk', 'fk_company', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'phone_number')


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
    class Meta:
        model = Building
        fields = (
            'id',
            'country',
            'address',
            'vicinity',
            'postcode',
            'building_name',
            'building_code',
        )


class NewBuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = (
            'country',
            'address',
            'vicinity',
            'postcode',
            'building_name',
        )

class DietBuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = (
            'id',
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
            'id',
            'fk_parent_category',
            'fk_priority',
            'label',
        )
        depth = 2


class CompanySerializer(serializers.ModelSerializer):
    fk_suitableEventCategories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = (
            'pk',
            'fk_suitableEventCategories',
            'country',
            'address',
            'vicinity',
            'postcode',
            'phone_number',
            'name',
            'vat_number',
        )


class CompanyListEntrySerializer(serializers.ModelSerializer):
    distance = serializers.FloatField()

    class Meta:
        model = Company
        fields = (
            'pk',
            'name',
            'distance',
        )


class FullTicketSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    fk_building = NewBuildingSerializer(many=False, read_only=True)
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
            'id',
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
            'description',
        )


class NewTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            'fk_category',

        )


class TicketCommentDietSerializer(serializers.Serializer):
    comment = serializers.CharField()
    date_created = serializers.DateTimeField()
    commenter_name = serializers.CharField()


class TicketCommentSerializer(serializers.ModelSerializer):
    fk_ticket_id = serializers.IntegerField()
    fk_commenter_id = serializers.IntegerField()

    class Meta:
        model = TicketComment
        fields = (
            'fk_ticket_id',
            'fk_commenter_id',
            'date_created',
            'comment',
        )


class TicketHistoryDietSerializer(serializers.Serializer):
    new_status = serializers.CharField()
    update_date = serializers.DateTimeField()
    update_reason = serializers.CharField()


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

class PlainResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    reason = serializers.CharField()


class UpdateTicketProgressionSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    reason = serializers.CharField()
    new_ticket_status = serializers.CharField()


class SuitableCompanySerializer(serializers.Serializer):
    company = CompanySerializer(many=False, read_only=True)
    distance = serializers.FloatField()