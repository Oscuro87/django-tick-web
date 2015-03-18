from django.db import models
from django.utils.translation import ugettext as _

from login.models import TicketsUser
from ticketing.custom_exceptions.TodoException import TodoException
from django.contrib import messages


"""
Représente le statut d'un ticket.
Valeurs prédéfinies: "Open" "In progress" "Closed"
"""


class TicketStatus(models.Model):
    label = models.CharField(verbose_name=_("Status"), max_length=64, null=False, blank=False)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name_plural = _("Ticket statuses")


"""
Représente la priorité d'un ticket.
Valeurs prédéfinies: "Low", "Medium", "High"
"""


class TicketPriority(models.Model):
    label = models.CharField(verbose_name=_("Priority"), max_length=64, null=False, blank=False)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name_plural = _("Ticket priorities")


"""
Le moyen de création du ticket.
Valeurs prédéfinies: "Web", "Phone", "Android"
"""


class Channel(models.Model):
    label = models.CharField(verbose_name=_("Way of ticket creation"), max_length=64, null=False, blank=False)

    def __str__(self):
        return self.label


"""
Représente un bâtiment dans lequel un ou plusieurs utilisateurs se trouvent.
"""


class Building(models.Model):
    address = models.CharField(verbose_name=_("Street"), max_length=45, blank=False, null=False, unique=True)
    vicinity = models.CharField(verbose_name=_("Vicinity name"), max_length=45, blank=False, null=False, default="")
    postcode = models.IntegerField(verbose_name=_("Postcode"), null=False, blank=False, default="0")
    building_name = models.CharField(verbose_name=_("Building name"), max_length=45, blank=False, null=False,
                                     unique=True, default="")
    building_code = models.CharField(verbose_name=_("Building code"), max_length=4, null=False, blank=False,
                                     unique=True, default="")
    visible = models.BooleanField(verbose_name=_("Is visible?"), null=False, blank=False, default=True)

    def __str__(self):
        return self.building_name + " (" + self.building_code + ")"

    class Meta:
        verbose_name_plural = _("Buildings")
        ordering = ["building_name", ]


class Place(models.Model):
    """
    Fais le lien entre un utilisateur et un bâtiment.
    """
    fk_building = models.ForeignKey(Building)
    fk_renter = models.OneToOneField(TicketsUser)
    visible = models.BooleanField(verbose_name=_("Is visible?"), default=True, null=False, blank=False)

    def __str__(self):
        return "" + self.fk_renter.get_full_name() + " @ " + self.fk_building.building_name


class CompanyManager(models.Manager):
    def get_companies_for_event_category(self, category):
        try:
            assert isinstance(category, EventCategory)
            if category.fk_company is not None:
                return Company.objects.filter(pk=category.fk_company_id)
            elif category.fk_company is None and category.fk_parent_category is not None:
                if category.fk_parent_category.fk_company is not None:
                    return Company.objects.filter(pk=category.fk_parent_category.fk_company_id)
                else:
                    return Company.objects.none()
            else:
                return Company.objects.none()
        except AssertionError:
            return Company.objects.none()


class Company(models.Model):
    """
    Représente une entreprise pouvant être appelée par un gestionnaire de ticket pour résoudre un problème.
    """
    fk_event_category = models.ForeignKey('EventCategory', null=True, blank=True, default=None)
    address = models.CharField(verbose_name=_("Street"), max_length=45, blank=False, null=False, unique=True)
    vicinity = models.CharField(verbose_name=_("Vicinity name"), max_length=45, blank=False, null=False, default="")
    postcode = models.IntegerField(verbose_name=_("Postcode"), null=False, blank=False, default="0")
    phone_number = models.CharField(verbose_name=_("Telephone number"), max_length=45, blank=True, null=True,
                                    default="")
    name = models.CharField(verbose_name=_("Company name"), max_length=45, null=False, blank=False)
    vat_number = models.CharField(verbose_name=_("VAT Number"), max_length=45, null=False, blank=False, unique=True)
    visible = models.BooleanField(verbose_name=_("Is visible?"), null=False, blank=False, default=True)

    def __str__(self):
        return self.name + " (" + self.vat_number + ")"

    class Meta:
        verbose_name_plural = "Companies"

    def get_all_companies_for_category(self, category):
        raise TodoException()
        # TODO récupérer les entreprises en fonction de la catégorie passée en param


class EventCategory(models.Model):
    """
    Représente soit une catégorie, soit une sous-catégorie d'évènement.
    """
    label = models.CharField(verbose_name=_("Incident label"), max_length=45, blank=False, null=False)
    visible = models.BooleanField(verbose_name=_("Is visible?"), null=False, blank=False, default=True)
    fk_parent_category = models.ForeignKey('self', null=True, blank=True, default=None)
    fk_priority = models.ForeignKey(TicketPriority, null=False)
    fk_company = models.ForeignKey(Company, null=True, blank=True, default=None)

    def __str__(self):
        if self.fk_parent_category is not None:
            return "" + self.label + " (parent: " + self.fk_parent_category.label + ")"
        else:
            return self.label + " (no parent)"

    def getAllSubCategories(self):
        if self.fk_parent_category == None:
            stuff = EventCategory.objects.filter(fk_parent_category__exact=self.pk)
            return stuff
        else:
            raise RuntimeError(_("This is not a parent category and therefore can't have sub-categories!"))

    def getParentCategory(self):
        if self.fk_parent_category is None:
            return self
        else:
            return self.fk_parent_category

    class Meta:
        verbose_name_plural = _("Event categories")


class TicketComment(models.Model):
    """
    Commentaire d'un ticket
    """
    fk_ticket = models.ForeignKey('Ticket', verbose_name="Ticket", null=False, blank=False, default=None)
    fk_commenter = models.ForeignKey(TicketsUser, verbose_name=_("Commenter"), null=False, blank=False, default=None)
    date_created = models.DateTimeField(verbose_name=_("Comment date"), blank=True, null=True, auto_now_add=True)
    comment = models.TextField(verbose_name=_("Comment"), blank=False, null=False, default="No comment provided.")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        self.__sendEmailToCommenters()

    def __sendEmailToCommenters(self):
        relatedComments = TicketComment.objects.filter(fk_ticket=self.fk_ticket)
        sendList = list()
        for comment in relatedComments:
            user = comment.fk_commenter
            if user not in sendList:
                sendList.append(user)
        for user in sendList:
            assert isinstance(user, TicketsUser)
            subject = "A comment has been posted on one of your tickets"
            message = "<p>The following ticket has a new comment: {}</p>" \
                      "<p>The comment is: \"{}\"</p>".format(self.fk_ticket.ticket_code, self.comment)
            try:
                user.email_user(subject, message)
            except ConnectionRefusedError:
                print("Cannot send email to commenters, connection to email provider is impossible.")

    def __str__(self):
        return "" + self.fk_commenter.get_full_name() + " commented on " + self.date_created.__str__() + " for ticket id " + self.fk_ticket.ticket_code


class Ticket(models.Model):
    """
    Représente un ticket.
    """
    fk_building = models.ForeignKey(Building, verbose_name=_("Building"), null=True, blank=True)
    fk_channel = models.ForeignKey(Channel, verbose_name=_("Channel"), null=False, blank=False)
    fk_category = models.ForeignKey(EventCategory, verbose_name=_("Category"), null=False, blank=False)
    fk_reporter = models.ForeignKey(TicketsUser, verbose_name=_("Reporter"), related_name="rapporteur", null=False,
                                    blank=False)
    fk_priority = models.ForeignKey(TicketPriority, verbose_name=_("Priority"), null=False, blank=False)
    fk_status = models.ForeignKey(TicketStatus, verbose_name=_("Status"), null=False, blank=False, default=1)

    ticket_code = models.CharField(verbose_name=_("Ticket code"), max_length=10, null=False, blank=True, unique=True)
    fk_manager = models.ForeignKey(TicketsUser, verbose_name=_("Manager"), related_name="gestionnaire", null=True,
                                   blank=True)
    fk_company = models.ForeignKey(Company, verbose_name=_("Company"), null=True, blank=True)
    floor = models.CharField(max_length=45, null=True, blank=True, default="")
    office = models.CharField(max_length=45, null=True, blank=True, default="")
    visible = models.BooleanField(verbose_name=_("Is visible?"), null=False, blank=False, default=True)
    intervention_date = models.DateField(verbose_name=_("Date of intervention"), null=True, blank=True, default=None)
    description = models.TextField(verbose_name=_("Event description"), null=True, blank=True,
                                   default=_("No description available."))

    def delete(self, using=None):
        self.visible = False
        self.save(reason="Ticket soft deletion.")

    def save(self, *args, **kwargs):
        reason = kwargs.pop('reason', None)

        if not self.ticket_code:
            self.ticket_code = self.__generateTicketCode()

        super(Ticket, self).save(*args, **kwargs)

        th = TicketHistory()
        th.fk_manager = self.fk_manager
        th.fk_ticket = self
        th.fk_ticket_status = self.fk_status
        if reason != None:
            th.update_reason = reason
        th.save()


    def __generateTicketCode(self):
        """
        Génère un code ticket unique
        :returns Le nombre de tickets existants pour le bâtiment assigné à ce ticket
        """
        if self.fk_building != None:
            count = self.__countAmountOfTicketsForBuilding() + 1
            code = self.fk_building.building_code + "-" + str(count)
        else:
            count = self.__countAmountOfBuildinglessTickets() + 1
            code = "NOBLD-" + str(count)
        return code

    def __countAmountOfBuildinglessTickets(self):
        return len(Ticket.objects.filter(fk_building__exact=None))

    def __countAmountOfTicketsForBuilding(self):
        return len(Ticket.objects.filter(fk_building__exact=self.fk_building.pk))

    def getTicketHistory(self):
        return TicketHistory.objects.filter(fk_ticket=self)

    def getAllTicketComments(self):
        return TicketComment.objects.filter(fk_ticket=self).order_by("-date_created")

    def setTicketManager(self, manager):
        self.fk_manager = manager
        self.save(reason=_("Assigned to manager: {}".format(manager.get_full_name())))
        return self

    def releaseTicketManagement(self):
        self.fk_manager = None
        self.save(reason=_("Manager released ticket management."))
        return self

    def changeTicketStatus(self, targetStatus):
        self.fk_status = targetStatus
        self.save(reason=_("Ticket status changed to {}".format(targetStatus.label)))
        return self

    def createComment(self, commenter, message):
        newComment = TicketComment()
        newComment.comment = message
        newComment.fk_commenter = commenter
        newComment.fk_ticket = self
        newComment.save()
        return newComment

    def __str__(self):
        ret = "Ticket " + self.ticket_code + " created by " + self.fk_renter.get_full_name()
        if self.fk_manager is not None:
            ret += " managed by " + self.fk_manager.get_full_name()
        else:
            ret += ", not managed by anyone."
        return ret


"""
Représente l'historique ticket dans lequel chaque opération sur un ticket est enregistrée, avec une raison.
"""


class TicketHistory(models.Model):
    update_date = models.DateTimeField(verbose_name=_("Updated on..."), blank=True, null=False, auto_now_add=True)
    update_reason = models.CharField(verbose_name=_("Update reason"), max_length=200, blank=True, null=False,
                                     default=_("No reason given."))
    fk_ticket = models.ForeignKey(Ticket, null=False, blank=False, on_delete=models.CASCADE)
    fk_ticket_status = models.ForeignKey(TicketStatus, null=False, blank=False)
    fk_manager = models.ForeignKey(TicketsUser, verbose_name=_("Who changed the status"), null=True,
                                   blank=True)

    class Meta:
        verbose_name_plural = "Ticket histories"

    def __str__(self):
        return "" + self.fk_ticket.ticket_code + " changed to " \
               + self.fk_ticket_status.label + " on " + str(self.update_date)

    """
    :returns Une liste d'historiques, tous tickets confondus, avec une limite d'entrées maximale à récupérer.
    """
    # TODO get_history_with_limit(self, limit=None)
    def getHistoryWithLimit(self, limit=None):
        raise TodoException()
