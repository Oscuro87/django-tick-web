from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import AnonymousUser
from django.contrib import auth
from rest_framework.views import APIView

from login.models import TicketsUser
from restserver.serializers import UserSerializer, SimpleTicketSerializer, FullTicketSerializer, \
    TicketCommentDietSerializer, TicketHistoryDietSerializer, TicketCommentSerializer, PlainResponseSerializer, \
    NewBuildingSerializer, CategorySerializer, BuildingSerializer, TicketStatusSerializer, CompanyListEntrySerializer
from ticketing.models import Ticket, TicketComment, TicketHistory, Place, EventCategory, Channel, TicketStatus, Company


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
        data["is_staff"] = user.isAdmin()
        for key, val in UserSerializer(user).data.items():
            data[key] = val

        return data


class RESTLogout(APIView):
    """
    Classe permettant à l'utilisateur de se déconnecter.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        return self.__processLogout()

    def __processLogout(self):
        if self.request.user.is_authenticated():
            # Destruction token?
            # Déco
            auth.logout(self.request)
            return Response({"disconnected": True})
        else:
            return Response({"disconnected": False})


class RESTSimpleTicketList(APIView):
    """
    Classe retournant la version simplifiée de tous les tickets d'un utilisateur.
    Ceci permet une transaction plus légère entre le client et ce serveur, lorsque toutes les informations
                                                                                        ticket ne sont pas nécéssaires.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        data = {}

        if "ticketType" in request.POST:
            assert isinstance(user, TicketsUser)
            data = self.__gatherUserTickets(user)

        return Response(data)

    def __gatherUserTickets(self, user):
        answer = {
            "user_tickets": list(),  # Les tickets de l'utilisateur courant
            "managed_by_user": list(),  # Les tickets gérés par l'utilisateur courant (s'il est gestionnaire)
            "unmanaged": list(),  # Les tickets gérés par aucun gestionnaire (et donc dispos pour gestion)
        }
        allTickets = Ticket.objects.all()

        # Si l'user est admin, on ajoute les tickets managés / non managés
        if user.isAdmin():
            # Unmanaged tickets
            closed = TicketStatus.objects.get(label="Closed")
            unmanaged = allTickets.filter(fk_manager=None).exclude(visible=False).exclude(fk_status=closed)
            managedByUser = allTickets.filter(fk_manager=self.request.user)

            for unmanagedTicket in unmanaged:
                serialized = SimpleTicketSerializer(unmanagedTicket)
                answer["unmanaged"].append(serialized.data)

            for managedTicket in managedByUser:
                serialized = SimpleTicketSerializer(managedTicket)
                answer["managed_by_user"].append(serialized.data)

        result = allTickets.filter(fk_reporter__exact=user)
        for tick in result:
            tickRedux = SimpleTicketSerializer(tick)
            answer["user_tickets"].append(tickRedux.data)

        # return data with tickets corresponding to user position
        return answer


class RESTFullTicket(APIView):
    """
    Cette classe retourne les informations complètes pour un seul ticket.
    La primary key du ticket requis est passé dans la requête REST sous l'identifiant "ticketPK".
    Si cet identifiant n'est pas présent, ou que le ticket n'est pas trouvé dans la DB, retourne une erreur 401.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if "ticketCode" in request.POST:
            ticketCode = request.POST.get('ticketCode', None)
            try:
                ticketObject = Ticket.objects.get(ticket_code=str(ticketCode))
                serializedTicket = FullTicketSerializer(ticketObject)
                return Response(serializedTicket.data, status=200)
            except ObjectDoesNotExist:
                return Response({"success": False, "reason": "Ticket not found"}, status=404)
        return Response({"success": False, "reason": "Unauthorized action!"}, status=501)


class RESTFullTicketComment(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if "ticketCode" in request.POST:
            code = request.POST.get('ticketCode', None)
            try:
                pk = _getTicketPKByCode(code)
                # orderby date_created DESC LIMIT 10
                commentsQueryset = TicketComment.objects.filter(fk_ticket=pk).order_by('-date_created')[:10]
                commentsEssentialInfos = list()
                for comm in commentsQueryset.all():
                    assert isinstance(comm, TicketComment)
                    comment = {"comment": comm.comment, "date_created": comm.date_created,
                               "commenter_name": comm.fk_commenter.get_full_name()}
                    commentsEssentialInfos.append(comment)
                serializedComments = TicketCommentDietSerializer(commentsEssentialInfos, many=True)
                return Response(serializedComments.data, status=200)
            except ObjectDoesNotExist:
                return Response({"success": False, "reason": "This ticket does not exist."}, status=404)
        return Response({"success": False, "reason": "Invalid send method."}, status=500)


class RESTCreateTicketComment(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        responseData = {}
        if "commentCreation" in request.data:
            serializer = TicketCommentSerializer(data=request.data)
            if (serializer.is_valid(False)):
                serializer.save()
                responseData = {"success": True, "reason": "Comment created."}
            else:
                responseData = {"success": False, "reason": "The comment was malformed."}
        else:
            responseData = {"success": False, "reason": "Problem saving the ticket's comment."}
        serializedResponseData = PlainResponseSerializer(responseData)
        return Response(serializedResponseData.data, status=200)


class RESTFullTicketHistory(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if "ticketCode" in request.POST:
            code = request.POST.get('ticketCode', None)
            try:
                pk = _getTicketPKByCode(code)
                historyQueryset = TicketHistory.objects.filter(fk_ticket=pk).order_by('-update_date')[:10]
                historyRedux = list()
                for hist in historyQueryset.all():
                    history = {"new_status": hist.fk_ticket_status.label, "update_date": hist.update_date,
                               "update_reason": hist.update_reason}
                    historyRedux.append(history)
                serializedHistory = TicketHistoryDietSerializer(historyRedux, many=True)
                return Response(serializedHistory.data, status=200)
            except ObjectDoesNotExist as odne:
                return Response({'success': False, 'reason': odne.__str__()}, status=404)
        else:
            return Response({"success": False, "reason": "Invalid method or request."}, status=500)


class RESTCreateBuilding(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        serializedBuilding = NewBuildingSerializer(data=request.data)
        try:
            if serializedBuilding.is_valid():
                place = Place()
                savedBuilding = serializedBuilding.save()
                place.fk_building = savedBuilding
                place.fk_owner = request.user
                place.save()
                return Response({"success": True, "reason": "Building created."}, status=200)
            else:
                reasons = ""
                for key, errorMessage in serializedBuilding.errors.items():
                    reasons += "{} : {}\n".format(key, errorMessage[0])
                return Response({"success": False, "reason": reasons}, status=200)
        except IntegrityError as ie:
            return Response({"success": False, "reason": "{}".format(ie.__cause__)}, status=200)


class RESTQueryCategories(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        result = self.__gatherCategories()
        return Response(result, status=200)

    def __gatherCategories(self):
        categories = EventCategory.objects.filter(fk_parent_category=None)
        subcategories = EventCategory.objects.all().exclude(fk_parent_category=None)
        result = {"categories": list(), "subcategories": list()}
        for cat in categories:
            result["categories"].append(CategorySerializer(cat).data)
        for subcat in subcategories:
            result["subcategories"].append(CategorySerializer(subcat).data)
        return result


class RESTQueryAllBuildings(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        buildings = self.__gatherUserBuildings()
        return Response(buildings, status=200)


    def __gatherUserBuildings(self):
        places = Place.objects.filter(fk_owner=self.request.user).exclude(visible=False)
        results = {"buildings": list()}

        for place in places.all():
            serialized = BuildingSerializer(place.fk_building)
            results["buildings"].append(serialized.data)
        return results


class RESTCreateTicket(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        t = Ticket()

        channel = Channel.objects.get(label="Android")
        t.fk_channel = channel

        creator = request.user
        t.fk_reporter = creator

        description = request.data.get('description', '')
        t.description = description

        office = request.data.get('office', None)
        t.office = office

        floor = request.data.get('floor', None)
        t.floor = floor

        building = request.data.get('building', None)
        if building is not None:
            t.fk_building_id = building["id"]
        else:
            t.fk_building = None

        category = request.data.get('category', None)
        if category is None:
            return Response({"success": False, "reason": "Ticket needs a category."}, status=200)
        else:
            cat = EventCategory.objects.get(id=category["id"])
            t.fk_category = cat

        t.fk_priority = t.fk_category.fk_priority
        t.fk_status = TicketStatus.objects.first()

        t.save()

        return Response({"success": True, "reason": "Ticket created"}, status=200)


class RESTUpdateDetails(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        print(request.data)
        ticketCode = request.data.get('ticket_code')
        ticket = Ticket.objects.get(ticket_code=ticketCode)

        newManager = request.data.get('fk_manager', None)
        if newManager is not None:
            ticketsUser = TicketsUser.objects.get(pk=newManager['pk'])
            ticket.fk_manager = ticketsUser
        else:
            ticket.fk_manager = None

        newCompany = request.data.get('fk_company', None)
        if newCompany is not None:
            companyInstance = Company.objects.get(pk=newCompany['pk'])
            ticket.fk_company = companyInstance
        else:
            ticket.fk_company = None

        ticket.save()

        return Response({"success": True, "reason": "Ticket details updated"}, status=200)


class RESTUpdateTicketProgression(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        ticketCode = request.data.get('ticketCode', None)
        if ticketCode is not None:
            return self.processNextTicketStatus(ticketCode)
        else:
            return Response({'success': False, 'reason': 'Ticket code provided was not correct'}, status=200)

    def processNextTicketStatus(self, ticketCode):
        try:
            ticketInstance = Ticket.objects.get(ticket_code=ticketCode)

            ticketStatuses = TicketStatus.objects.all()
            newTicketStatusInstance = ticketInstance.fk_status
            changeNext = False
            for status in ticketStatuses.all():
                if changeNext:
                    newTicketStatusInstance = status
                    break
                if ticketInstance.fk_status == status:
                    changeNext = True

            ticketInstance.fk_status = newTicketStatusInstance

            print(ticketInstance.fk_status.label)

            ticketInstance.save(reason="Updated ticket status via REST")

            answer = {
                "success": True,
                "reason": "Ticket status updated",
                "new_ticket_status": TicketStatusSerializer(newTicketStatusInstance).data
            }

            return Response(answer, status=200)
        except ObjectDoesNotExist as odne:
            return Response({'success': False, 'reason': odne.__str__()}, status=200)

            # print(ticketCode)


################ Méthodes communes à toutes les classes ####################"

def _getTicketPKByCode(ticketCode):
    if ticketCode is None:
        return None
    else:
        return Ticket.objects.get(ticket_code=ticketCode).pk


class RESTGetListOfCompanies(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        ticketCode = request.data.get('ticketCode', None)

        if ticketCode is not None:
            return self.buildCompaniesList(ticketCode)
        else:
            answer = {
                'succes': False,
                'reason': 'Ticket code was not provided!',
            }
            return Response(answer, status=200)

    def buildCompaniesList(self, ticketCode):
        ticketInstance = Ticket.objects.get(ticket_code=ticketCode)
        companies = ticketInstance.getAllSuitableCompanies()

        serializedCompanies = [{'pk': -1, 'name': "", 'distance': 0}]

        for entry in companies:
            company = CompanyListEntrySerializer({'pk': entry[0].pk, 'name': entry[0].name, 'distance': entry[1]})
            serializedCompanies.append(company.data)

        answer = {
            "success": True,
            "reason": "Retrieved companies list",
            "companies": serializedCompanies,
        }

        return Response(answer, status=200)


class RESTUpdateTicketCompany(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        ticketCode = request.data.get('ticketCode', None)
        companyPK = CompanyListEntrySerializer(request.data.get('company', None)).data.pk

        self.processAssociation(ticketCode, companyPK)

    def processAssociation(self, ticketCode, companyPK):
        try:
            ticketInstance = Ticket.objects.get(ticket_code=ticketCode)
            companyInstance = None
            if companyPK is not None:
                if companyPK != -1:
                    companyInstance = Company.objects.get(pk=companyPK)

            ticketInstance.fk_company = companyInstance

            if companyInstance is not None:
                ticketInstance.save("Changed assigned company to {}".format(companyInstance.name))
            else:
                ticketInstance.save("Unassigned company from ticket")

            answer = {
                'success': True,
                'reason': 'Company successfully assigned to ticket',
            }

            return Response(answer, status=200)
        except ObjectDoesNotExist as error:
            answer = {
                'success': False,
                'reason': error.__str__(),
            }
            return Response(answer, status=200)