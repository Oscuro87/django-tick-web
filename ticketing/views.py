import json

from django.shortcuts import HttpResponse, render_to_response, RequestContext, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser
from django.contrib import messages
from django.utils.translation import ugettext as _
from ticketing.custom_exceptions.TicketCreationException import TicketCreationException

from ticketing.forms import ContactForm, TicketCommentForm
from ticketing.models import EventCategory, Ticket, TicketStatus


class ContactView(TemplateView):
    template_name = "ticketing/contact.html"

    def get(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            return redirect('loginview')

        return self.showPlainContactForm()

    def post(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            return redirect('loginview')

        return self.showPlainContactForm()

    def showPlainContactForm(self):
        data = dict()
        data['contact_form'] = ContactForm()
        data['user_info'] = self.request.user

        return render_to_response(self.template_name, data, RequestContext(self.request))


class CreateTicketView(TemplateView):
    template_name = "ticketing/create_ticket.html"

    def get(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            return redirect('loginview')

        return self.renderPlainCTView()

    def post(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
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
            messages.add_message(self.request, messages.SUCCESS, "You successfully created a ticket!")
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
        channelID = 1  # Web
        statusID = 1  # open
        if subcategoryID != 'empty':
            priorityID = EventCategory.objects.get(pk=subcategoryID).fk_priority.pk
        else:
            priorityID = EventCategory.objects.get(pk=categoryID).fk_priority.pk
        floor = self.request.POST.get('floor')
        office = self.request.POST.get('office')
        description = self.request.POST.get('description')

        t = Ticket()
        t.fk_building_id = batimentID
        if(subcategoryID != 'empty'):
            t.fk_category_id = subcategoryID
        else:
            t.fk_category_id = categoryID
        t.fk_reporter_id = creatorID
        t.fk_channel_id = channelID
        t.fk_status_id = statusID
        t.fk_priority_id = priorityID
        t.floor = floor
        t.office = office
        t.description = description

        return t


class HomeView(TemplateView):
    template_name = "ticketing/index.html"

    def get(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            return redirect('loginview')

        return self.showPlainHomeView()

    def post(self, request, *args, **kwargs):
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
                selection = selection.filter(Q(fk_manager=self.request.user) | Q(fk_manager=None))

            if not self.request.session.get('show_closed_tickets'):
                fk_status_closed = TicketStatus.objects.get(label="Closed")
                selection = selection.exclude(fk_status__exact=fk_status_closed)
            data['all_queried_tickets'] = selection
        else:
            selection = Ticket.objects.filter(visible__exact=True)
            selection = selection.filter(fk_reporter__exact=self.request.user)
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

        if "ticket_id" in kwargs:
            return self.show(kwargs['ticket_id'])

        return redirect('homeview')

    def post(self, request, *args, **kwargs):
        if "ticket-release" in request.POST:
            return self.releaseTicketManagement()

        if "ticket_id" in request.POST:
            if "ticket-to-inProgress" in request.POST:
                return self.processTicketStatusChange("In progress")
            elif "ticket-to-closed" in request.POST:
                return self.processTicketStatusChange("Closed")
            elif "comment-body" in request.POST:
                return self.createNewTicketComment()
            else:
                theID = self.request.POST.get('ticket_id')
                return self.show(theID)

        return redirect('homeview')

    def show(self, ticket_id):
        data = dict()

        data['user_info'] = self.request.user

        try:
            ticket_obj = Ticket.objects.get(pk=ticket_id)
            assert isinstance(ticket_obj, Ticket)
            """
            if ticket_obj.fk_manager != self.request.user:
                messages.add_message(self.request, messages.ERROR,
                                     _("You are not managing this ticket, so you cannot see its details."))
                return redirect('homeview')
            """

            data['ticket'] = ticket_obj
            data['ticket_history'] = ticket_obj.getTicketHistory()
            data['ticket_comments'] = ticket_obj.getAllTicketComments()
            data['comment_form'] = TicketCommentForm()

            return render_to_response(self.template_name, data, RequestContext(self.request))
        except Ticket.DoesNotExist:
            messages.add_message(self.request, messages.ERROR, _("This ticket ID {0} doesn't exist.".format(ticket_id)))
            return redirect('homeview')

    def createNewTicketComment(self):
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