import json
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import HttpResponse, render_to_response, RequestContext, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser
from django.contrib import messages
from django.utils.translation import ugettext as _
from login.models import TicketsUserManager, TicketsUser
from ticketing.custom_exceptions.TicketCreationException import TicketCreationException

from ticketing.forms import ContactForm, TicketCommentForm, BuildingCreationForm, CompanyUpdateForm, \
    UpdateBuildingSelectorForm, UpdateBuildingForm
from ticketing.models import EventCategory, Ticket, TicketStatus, Building, Place, Channel


class ContactView(TemplateView):
    template_name = "ticketing/contact.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('loginview')

        return self.showPlainContactForm()

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('loginview')

        if "contactSend" in request.POST:
            return self.__processSendContactMessage()

        return self.showPlainContactForm()

    def showPlainContactForm(self):
        data = dict()
        data['contact_form'] = ContactForm()

        return render_to_response(self.template_name, data, RequestContext(self.request))

    def __processSendContactMessage(self):
        print("Processing contact message")
        cf = ContactForm(data=self.request.POST)

        if cf.is_valid():
            messages.success(self.request, _("Your message has been sent to the administrators."))
            tum = TicketsUserManager()
            tum.sendContactMessageToAdmins(cf.cleaned_data['subject'], cf.cleaned_data['content'])
            return redirect("homeview")
        else:
            messages.error(self.request, _("Please fill the contact form completely."))
            return self.showPlainContactForm()


class CreateTicketView(TemplateView):
    template_name = "ticketing/create_ticket.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('loginview')

        return self.renderPlainCTView()

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('loginview')

        if "operation" in request.POST:
            if request.POST.get("operation") == "GETSUBCATEGORIES":
                return self.ajax_getSubCategoriesForCategory()

        if "ticketCreateGo" in request.POST:
            return self.doCreateTicket()

        return self.renderPlainCTView()

    def renderPlainCTView(self):
        data = dict()
        data['user_info'] = self.request.user

        return render_to_response(self.template_name, data, RequestContext(self.request))

    def ajax_getSubCategoriesForCategory(self):
        categoryID = self.request.POST.get('categoryID')
        returnData = dict()

        categoryObject = get_object_or_404(EventCategory, pk=categoryID)
        assert isinstance(categoryObject, EventCategory)
        subcats = categoryObject.getAllSubCategories()
        selection = []
        for item in subcats:
            assert isinstance(item, EventCategory)
            selection.append({
                'pk': item.pk,
                'label': item.label,
            })
        returnData['subcategories'] = selection

        return HttpResponse(json.dumps(returnData), content_type="application/json")

    def doCreateTicket(self):
        try:
            ticket = self.preBuildNewTicket()
            ticket.save(reason=_("Creating new ticket."))
            messages.add_message(self.request, messages.SUCCESS, _("You successfully created a ticket!"))
            return redirect('homeview')
        except TicketCreationException as err:
            messages.error(self.request, err.getMessage())
            return self.renderPlainCTView()

    def preBuildNewTicket(self):
        batimentID = self.request.POST.get('building')
        categoryID = self.request.POST.get('category')
        if categoryID == 'empty':
            raise TicketCreationException(_("The main category cannot be empty!"))
        subcategoryID = self.request.POST.get('subcategory')
        creatorID = self.request.user.pk
        channelInstance, created = Channel.objects.get_or_create(label="Web")  # Web
        statusInstance = TicketStatus.objects.first()  # open
        if subcategoryID != 'empty':
            priorityID = EventCategory.objects.get(pk=subcategoryID).fk_priority.pk
        else:
            priorityID = EventCategory.objects.get(pk=categoryID).fk_priority.pk
        floor = self.request.POST.get('floor')
        office = self.request.POST.get('office')
        description = self.request.POST.get('description')

        t = Ticket()
        t.fk_building_id = batimentID
        if t.fk_building_id == '':
            t.fk_building = None
        if subcategoryID != 'empty':
            t.fk_category_id = subcategoryID
        else:
            t.fk_category_id = categoryID
        t.fk_reporter_id = creatorID
        t.fk_channel = channelInstance
        t.fk_status = statusInstance
        t.fk_priority_id = priorityID
        t.floor = floor
        t.office = office
        t.description = description

        return t


class HomeView(TemplateView):
    template_name = "ticketing/index.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('loginview')

        if isinstance(request.user, AnonymousUser):
            return redirect('loginview')

        return self.showPlainHomeView()

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('loginview')

        self.checkRedirections()

        return self.showPlainHomeView()

    def checkRedirections(self):
        if isinstance(self.request.user, AnonymousUser):
            return redirect('loginview')

        if "switchTicketVisibility" in self.request.POST:
            if self.request.session.get('show_unrelated_tickets', False):
                self.request.session['show_unrelated_tickets'] = False
            else:
                self.request.session['show_unrelated_tickets'] = True

        if "switchClosedTicketVisibility" in self.request.POST:
            if self.request.session.get('show_closed_tickets', False):
                self.request.session['show_closed_tickets'] = False
            else:
                self.request.session['show_closed_tickets'] = True

        if "assigntickettome" in self.request.POST:
            return self.assignTicketToMe()

    def showPlainHomeView(self):
        data = dict()

        data['user_info'] = self.request.user

        if self.request.user.isAdmin():
            selection = Ticket.objects.filter(visible__exact=True)

            if not self.request.session.get('show_unrelated_tickets', False):
                selection = selection.filter(Q(fk_manager=self.request.user) | Q(fk_manager=None) | Q(fk_reporter=self.request.user))

            if not self.request.session.get('show_closed_tickets'):
                fk_status_closed = TicketStatus.objects.get(label="Closed")
                selection = selection.exclude(fk_status__exact=fk_status_closed)

            data['all_queried_tickets'] = selection
        else:
            selection = Ticket.objects.filter(visible__exact=True)
            if not self.request.user.isUserACompany():
                selection = selection.filter(fk_reporter__exact=self.request.user)
            else:
                selection = selection.filter(fk_company__exact=self.request.user.fk_company)
            data['all_queried_tickets'] = selection

            if not self.request.session.get('show_closed_tickets'):
                fk_status_closed = TicketStatus.objects.get(label="Closed")
                selection = selection.exclude(fk_status__exact=fk_status_closed)

            data['all_queried_tickets'] = selection

        return render_to_response(self.template_name, data, RequestContext(self.request))

    def assignTicketToMe(self):
        try:
            user = self.request.user
            code = self.request.POST.get('ticket_code')
            ticket = Ticket.objects.get(ticket_code=code)
            if ticket.fk_manager is None:
                ticket.setTicketManager(user)
            else:
                messages.add_message(self.request, messages.ERROR, _("This ticket is already assigned to someone!"))
        except Ticket.DoesNotExist:
            messages.add_message(self.request, messages.ERROR, _("This ticket {0} doesn't exist!".format(str(code))))

        return self.showPlainHomeView()


class TicketView(TemplateView):
    template_name = "ticketing/ticket_view.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('loginview')

        if "ticket_id" in kwargs:
            return self.show(kwargs['ticket_id'])

        return redirect('homeview')

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('loginview')

        if "ticket-release" in request.POST:
            return self.releaseTicketManagement()

        if "ticket_id" in request.POST:
            if "ticket-to-inProgress" in request.POST:
                return self.processTicketStatusChange("In progress")
            elif "ticket-to-closed" in request.POST:
                return self.processTicketStatusChange("Closed")
            elif "comment-body" in request.POST:
                return self.createTicketComment()
            elif "changeCompany" in request.POST:
                return self.changeTicketCompanyAssignment()
            else:
                theID = self.request.POST.get('ticket_id')
                return self.show(theID)

        return redirect('homeview')

    def show(self, ticket_id):
        data = dict()

        data['user_info'] = self.request.user

        try:
            ticket_obj = Ticket.objects.get(pk=ticket_id)

            data['suitableCompanies'] = ticket_obj.getAllSuitableCompanies()
            data['ticket'] = ticket_obj
            data['ticket_history'] = ticket_obj.getTicketHistory()
            data['ticket_comments'] = ticket_obj.getAllTicketComments()
            data['comment_form'] = TicketCommentForm()

            return render_to_response(self.template_name, data, RequestContext(self.request))
        except Ticket.DoesNotExist:
            messages.add_message(self.request, messages.ERROR, _("This ticket ID {0} doesn't exist.".format(ticket_id)))
            return redirect('homeview')

    def createTicketComment(self):
        request = self.request
        ticketID = self.request.POST.get('ticket_id')
        ticketObject = Ticket.objects.get(pk=ticketID)
        assert isinstance(ticketObject, Ticket)
        if ticketObject != None:
            commentBody = self.request.POST.get('comment-body', "No comment body!")
            ticketObject.createComment(request.user, commentBody)
            messages.success(request, _("The comment has been posted."))
        else:
            messages.error(request, _("This ticket does not exist!"))
            return redirect("homeview")

        return self.show(ticketID)

    def releaseTicketManagement(self):
        ticket_id = self.request.POST.get('ticket_id')
        try:
            ticket_obj = Ticket.objects.get(pk=ticket_id)
            assert isinstance(ticket_obj, Ticket)
            ticket_obj.releaseTicketManagement()
            messages.add_message(self.request, messages.SUCCESS, _("You no longer manage this ticket."))

            return redirect('homeview')
        except Ticket.DoesNotExist:
            messages.add_message(self.request, messages.ERROR, _("Cannot execute this action."))
            return self.show(ticket_id)

    def processTicketStatusChange(self, to):
        ticket_id = self.request.POST.get('ticket_id')
        try:
            ticket_obj = Ticket.objects.get(pk=ticket_id)
            status_obj = TicketStatus.objects.get(label=to)
            assert isinstance(ticket_obj, Ticket)
            ticket_obj.changeTicketStatus(status_obj)
            messages.add_message(self.request, messages.SUCCESS, _("Ticket successfully updated."))
        except Ticket.DoesNotExist:
            messages.add_message(self.request, messages.ERROR, _("Cannot execute this action."))
        except TicketStatus.DoesNotExist:
            messages.add_message(self.request, messages.ERROR, _("Cannot execute this action."))

        return self.show(ticket_id)

    def changeTicketCompanyAssignment(self):
        ticket_id = self.request.POST.get('ticket_id')
        company_id = self.request.POST.get('changeCompany')
        try:
            ticket_obj = Ticket.objects.get(pk=ticket_id)
            ticket_obj = ticket_obj.changeCompanyAssignment(company_id)
            messages.success(self.request, _("You successfully changed the company assigned to this ticket."))
        except Ticket.DoesNotExist:
            messages.add_message(self.request, messages.ERROR, _("Cannot execute this action."))
        except TicketStatus.DoesNotExist:
            messages.add_message(self.request, messages.ERROR, _("Cannot execute this action."))

        return self.show(ticket_id)

class CreateLocationView(TemplateView):
    template_name = "ticketing/create_location.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('loginview')

        return self.show()

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('loginview')

        if "createBuilding" in request.POST:
            return self.createABuilding()

        if "createBuildingThenTicket" in request.POST:
            self.createABuilding()
            return redirect("createticketview")

        return self.show()

    def show(self):
        data = {}
        data["form"] = self.prepareBuildingCreationForm()

        return render_to_response(self.template_name, data, RequestContext(self.request))

    def prepareBuildingCreationForm(self):
        return BuildingCreationForm()

    def createABuilding(self):
        sourceForm = BuildingCreationForm(self.request.POST)
        if sourceForm.is_valid():
            newBuilding = sourceForm.save()
            # Il faut maintenant créer un nouveau "Place" pour assigner ce bâtiment à l'utilisateur qui l'a créé.
            newLocation = Place()
            newLocation.fk_building = newBuilding
            newLocation.fk_owner = self.request.user # = la personne qui l'a créé
            newLocation.save()
            messages.success(self.request, _("The building was created successfully."))
            return redirect("homeview")
        else:
            messages.error(self.request, _("There were errors in the form you filled, please try again."))
            return self.show()


class UpdateCompanyView(TemplateView):
    template_name = 'ticketing/update_company_view.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('loginview')

        return self.show()

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('loginview')

        if "doUpdateCompanyInfos" in self.request.POST:
            return self.processUpdate()

        if "cancelUpdateCompanyInfos" in self.request.POST:
            messages.info(request, _("You cancelled updating the company's informations."))
            return redirect("homeview")

        return self.show()

    def show(self):
        data = {}

        data['updateForm'] = CompanyUpdateForm(instance=self.request.user.fk_company)

        return render_to_response(self.template_name, data, RequestContext(self.request))

    def processUpdate(self):
        companyInstance = self.request.user.fk_company
        retrieveForm = CompanyUpdateForm(self.request.POST, instance=companyInstance)
        if retrieveForm.is_valid():
            retrieveForm.save()
            messages.success(self.request, _("You updated your company informations successfully."))
            return redirect("homeview")
        else:
            messages.error(self.request, _("Error in the form, please fill it in correctly."))
            return self.show()


class UpdateBuildingView(TemplateView):
    template_name = "ticketing/update_building_view.html"

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return redirect("loginview")

        return self.showSelectionPhase()

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return redirect("loginview")

        if "selected" in request.POST:
            return self.showUpdatePhase()

        if "doUpdate" in request.POST:
            return self.__processBuildingUpdate()

        if "cancelUpdate" in request.POST:
            return redirect("homeview")

        if "releaseOwnership" in request.POST:
            return self.__processReleaseOwnership()

        if "chooseAnother" in request.POST:
            pass

        return self.showSelectionPhase()

    def showUpdatePhase(self):
        try:
            building = Building.objects.get(pk=int(self.request.POST.get('building_selector')))
            buildingForm = UpdateBuildingForm(instance=building)

            data = {
                "buildingForm": buildingForm
            }

            return render_to_response(self.template_name, data, RequestContext(self.request))
        except ObjectDoesNotExist as odne:
            messages.error(self.request, _("Internal error while selecting the building to modify."))
            return self.showSelectionPhase()

    def showSelectionPhase(self):
        places = Place.objects.filter(fk_owner=self.request.user.id)
        buildings = []
        for place in places.all():
            buildings.append((place.fk_building.id, place.fk_building.building_name,))
        selectionForm = UpdateBuildingSelectorForm(buildings)

        data = {
            "selectionForm": selectionForm
        }

        return render_to_response(self.template_name, data, RequestContext(self.request))

    def __processReleaseOwnership(self):
        building = Building.objects.get(building_code=self.request.POST.get('building_code'))
        form = UpdateBuildingForm(data=self.request.POST, instance=building)

        if form.is_valid():
            place = Place.objects.get(Q(fk_owner=self.request.user) | Q(fk_building=building))
            place.delete()
            messages.success(self.request, _("Building ownership released"))
            return redirect("homeview")
        else:
            messages.error(self.request, _("An error occured during the update, please fill it in correctly."))
            return self.showSelectionPhase()

    def __processBuildingUpdate(self):
        building = Building.objects.get(building_code=self.request.POST.get('building_code'))
        form = UpdateBuildingForm(data=self.request.POST, instance=building)

        if form.is_valid():
            form.save()
            messages.success(self.request, _("Building informations updated successfully"))
            return redirect("homeview")
        else:
            messages.error(self.request, _("An error occured during the update, please fill it in correctly."))
            return self.showSelectionPhase()