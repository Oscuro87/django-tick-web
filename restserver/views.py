from django.contrib.sessions.models import Session
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import AnonymousUser
from django.contrib import auth
from rest_framework.views import APIView

from login.models import TicketsUser
from restserver.serializers import UserSerializer


class RESTLogin(APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        if isinstance(request.user, AnonymousUser):
            if "email" in request.POST and "password" in request.POST:
                user = auth.authenticate(email=request.POST.get('email'), password=request.POST.get('password'))
                if user is not None:
                    if user.is_active:
                        auth.login(request, user)
                        data = self.__buildResponseData(user)
                        return Response(data, content_type="application/json", status=200)
                    else:
                        return Response({"success": False, "reason": "User is banned."},
                                        content_type="application/json")
                else:
                    return Response({"success": False, "reason": "Wrong credentials!"}, content_type="application/json")

        return Response({"success": False, "reason": "Internal error."}, content_type="application/json")

    def __buildResponseData(self, user):
        data = {}
        assert isinstance(user, TicketsUser)
        token = Token.objects.get_or_create(user=user)[0]
        data["authtoken"] = token.key
        data["success"] = True
        data["reason"] = "Login successful"
        data["userdata"] = UserSerializer(user).data

        return data


class RESTLogout(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        return self.__processLogout()

    def __processLogout(self):
        if self.request.user.is_authenticated():
            auth.logout(self.request)
            return Response({"disconnected": True})
        else:
            return Response({"disconnected": False})


class RESTSimpleTicket(APIView):
    """
    Classe retournant la version simplifiée de tous les tickets d'un utilisateur.
    Ceci permet une transaction plus légère entre le client et ce serveur, lorsque toutes les informations
        ticket ne sont pas nécéssaires.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        pass

def _getUserBySessionKey(request, key):
    session = Session.objects.get(session_key=key)
    uid = session.get_decoded().get('_auth_user_id')
    user = TicketsUser.objects.get(pk=uid)
    request.user = user
    return user