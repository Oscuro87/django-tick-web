from login.models import TicketsUser
from rest_framework import serializers

class TicketsUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TicketsUser
        fields = ('firstName', 'lastName', 'email', 'isStaff', 'isActive', 'dateJoined', 'receiveNewsletter')