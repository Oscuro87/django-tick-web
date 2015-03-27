from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import AnonymousUser
from django.contrib import auth
from login.models import TicketsUser
from django.db.models import Q


@api_view(['POST'])
def rest_login(request):
    if isinstance(request.user, AnonymousUser):
        if request.method == 'POST':
            if "email" in request.POST and "password" in request.POST:
                user = auth.authenticate(email=request.POST.get('email'), password=request.POST.get('password'))
                if user is not None:
                    if user.is_active:
                        auth.login(request, user)
                        data = __buildDataForUser(user)
                        return Response(data, content_type="application/json", status=200)
                    else:
                        return Response({"success": False, "reason": "User is banned."}, content_type="application/json")
                else:
                    return Response({"success": False, "reason": "Wrong credentials!"}, content_type="application/json")

    return Response({"success": False, "reason": "Internal error."}, content_type="application/json")

def __buildDataForUser(user):
    data = {}
    data["success"] = True
    data["reason"] = "Login successful"
    data["email"] = user.email
    data["first_name"] = user.first_name
    data["last_name"] = user.last_name
    if len(TicketsUser.objects.filter(
        Q(is_superuser=True) |
        Q(groups__permissions__codename="root") |
        Q(groups__permissions__codename="manager"))
            .distinct()) != 0:
        data["is_staff"] = True
    else:
        data["is_staff"] = False
    return data


@api_view(['GET'])
def rest_logout(request):
    if request.method == "GET":
        if request.user.is_authenticated():
            auth.logout(request)
            return Response({"disconnected": True})
    return Response({"disconnected": False})