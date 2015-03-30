from login.models import TicketsUser
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TicketsUser
        fields = ('first_name', 'last_name', 'email', 'is_active', 'is_staff')
