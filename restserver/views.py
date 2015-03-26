from rest_framework import viewsets
from rest_framework.response import Response
from login.models import TicketsUser
from restserver.serializers import TicketsUserSerializer

class TicketsUserViewset(viewsets.ModelViewSet):
    data = TicketsUser.objects.all()
    serializer_class = TicketsUserSerializer

    def get(self, request, format=None):
        usernames = [user.username for user in TicketsUser.objects.all()]
        return Response(usernames)