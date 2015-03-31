from login.models import TicketsUser
from rest_framework import serializers
from ticketing.models import Ticket, TicketStatus


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