import os
from django.db import models
from django.utils.translation import ugettext as _
from django_countries.fields import CountryField
from django.core.mail import send_mail
from django.conf import settings

from login.models import TicketsUser
from ticketing.custom_exceptions.TodoException import TodoException
from geolocation.GeoPyInterface import GeoPyInterface, ResultType


class TicketStatus(models.Model):
    """
    Représente le statut d'un ticket.
    Valeurs prédéfinies: "Open" "In progress" "Closed"
    """
    label = models.CharField(verbose_name=_("Status"), max_length=64, null=False, blank=False)

    def __str__(self):
        return self.label


class Meta:
    verbose_name_plural = _("Ticket statuses")


class TicketPriority(models.Model):
    """
    Représente la priorité d'un ticket.
    Valeurs prédéfinies: "Low", "Medium", "High"
    """
    label = models.CharField(verbose_name=_("Priority"), max_length=64, null=False, blank=False)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name_plural = _("Ticket priorities")


class Channel(models.Model):
    """
    Le moyen de création du ticket.
    Valeurs prédéfinies: "Web", "Phone", "Android"
    """
    label = models.CharField(verbose_name=_("Way of ticket creation"), max_length=64, null=False, blank=False)

    def __str__(self):
        return self.label


class BuildingManager(models.Manager):
    def get_users_for_building(self, building_id):
        places = Place.objects.filter(fk_building__exact=building_id)
        users = list()
        for key, p in places:
            if not users.__contains__(p):
                users.append(p.fk_owner)
        return users


class Building(models.Model):
    """
    Représente un bâtiment dans lequel un ou plusieurs utilisateurs se trouvent.
    """
    country = CountryField(null=False)
    address = models.CharField(verbose_name=_("Street"), max_length=45, blank=False, null=False, unique=True)
    vicinity = models.CharField(verbose_name=_("Vicinity name"), max_length=45, blank=True, null=True, default="")
    city = models.CharField(verbose_name=_("City name"), max_length=45, blank=True, null=True, default="")
    postcode = models.CharField(verbose_name=_("Postcode"), null=True, blank=True, default="", max_length=10)
    building_name = models.CharField(verbose_name=_("Building name"), max_length=45, blank=False, null=False,
                                     unique=True, default="")
    building_code = models.CharField(verbose_name=_("Building code"), max_length=20, null=False, blank=True,
                                     unique=True, default="")
    visible = models.BooleanField(verbose_name=_("Is visible?"), null=False, blank=False, default=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        checkBuildingNameExists = Building.objects.filter(building_name=self.building_name)

        if len(checkBuildingNameExists) > 0 and self.building_name == "":
            self.building_name = self.getFullAddress()

        super().save(force_insert, force_update, using, update_fields)

        while self.building_code == "":
            self.building_code = self.createCode()
            self.save()

        return self

    def getFullAddress(self):
        return "{} {} {} {}".format(self.address, self.city, self.postcode, self.country)

    def createCode(self):
        result = self.building_code
        nameSplit = self.building_name.split(" ", 6)
        if len(nameSplit) != 1:
            for piece in nameSplit:
                result += piece[0]
        else:
            result = nameSplit[0]
        result += str(self.pk)
        return result

    def __str__(self):
        return self.building_name + " (" + self.building_code + ")"

    class Meta:
        verbose_name_plural = _("Buildings")
        ordering = ["building_name", ]


class Place(models.Model):
    """
    Fais le lien entre un utilisateur et un bâtiment.
    """
    fk_building = models.ForeignKey(Building, verbose_name="Building", unique=False, null=False, blank=False)
    fk_owner = models.ForeignKey(TicketsUser, verbose_name="Owner", unique=False, null=False, blank=False)
    visible = models.BooleanField(verbose_name=_("Is visible?"), default=True, null=False, blank=False)

    def __str__(self):
        return "{} @ {}".format(self.fk_owner.get_full_name(), self.fk_building.building_name)


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
    fk_suitableEventCategories = models.ManyToManyField("EventCategory", verbose_name=_("Suitable Event Categories"),
                                                        blank=True)
    country = CountryField(verbose_name=_("Country"))
    address = models.CharField(verbose_name=_("Street"), max_length=45, blank=False, null=False, unique=True)
    vicinity = models.CharField(verbose_name=_("Vicinity name"), max_length=45, blank=True, null=True, default="")
    city = models.CharField(verbose_name=_("City name"), max_length=60, blank=False, null=False, default="")
    postcode = models.IntegerField(verbose_name=_("Postcode"), null=False, blank=False, default="0")
    phone_number = models.CharField(verbose_name=_("Telephone number"), max_length=45, blank=True, null=True,
                                    default="")
    name = models.CharField(verbose_name=_("Company name"), max_length=45, null=False, blank=False)
    vat_number = models.CharField(verbose_name=_("VAT Number"), max_length=45, null=True, blank=True)
    visible = models.BooleanField(verbose_name=_("Is visible?"), null=False, blank=False, default=True)

    def __str__(self):
        return "{} | VAT: {} | Phone: {}".format(self.name, self.vat_number, self.phone_number)

    class Meta:
        verbose_name_plural = "Companies"


class EventCategory(models.Model):
    """
    Représente soit une catégorie, soit une sous-catégorie d'évènement.
    """
    fk_parent_category = models.ForeignKey('self', verbose_name="Parent category", null=True, blank=True, default=None)
    fk_priority = models.ForeignKey(TicketPriority, verbose_name="Priority", null=False)
    label = models.CharField(verbose_name=_("Incident label"), max_length=45, blank=False, null=False)
    visible = models.BooleanField(verbose_name=_("Is visible?"), null=False, blank=False, default=True)

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
            subject = _("A comment has been posted on one of your tickets")
            message = _("<p>The following ticket has a new comment: {}</p>"
                        "</p>The comment is: \"{}\"</p>"
                        "<p><a href=\"{}\">Ticketing platform</a></p>").format(self.fk_ticket.ticket_code, self.comment,
                                                                               settings.MY_EMAIL_SITE_LINK)
            try:
                send_mail(subject, "", "ticketing.platform@gmail.com", [user.email], fail_silently=False,
                          html_message=message)
            except ConnectionRefusedError as e:
                print("Cannot send email to commenters, connection to email provider is impossible: \n{}".format(
                    e.__str__()))

    def __str__(self):
        if self.fk_commenter is not None:
            return "{} commented on {} for ticket id {})".format(self.fk_commenter.get_full_name(),
                self.date_created.__str__(), self.fk_ticket.ticket_code)
        else:
            return "Problem"


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
    fk_manager = models.ForeignKey(TicketsUser, verbose_name=_("Manager"), related_name="gestionnaire", null=True,
                                   blank=True)
    fk_company = models.ForeignKey(Company, verbose_name=_("Company"), null=True, blank=True)

    image_folder_name = models.CharField(verbose_name=_("Name of this ticket's images folder"), max_length=128,
                                         null=True, blank=True)
    ticket_code = models.CharField(verbose_name=_("Ticket code"), max_length=10, null=False, blank=True, unique=True)
    floor = models.CharField(max_length=45, null=True, blank=True, default="")
    office = models.CharField(max_length=45, null=True, blank=True, default="")
    visible = models.BooleanField(verbose_name=_("Is visible?"), null=False, blank=False, default=True)
    intervention_date = models.DateField(verbose_name=_("Date of intervention"), null=True, blank=True, default=None)
    description = models.TextField(verbose_name=_("Event description"), null=True, blank=True,
                                   default=_("No description available."))

    def delete(self, using=None):
        # Ne pas appeler le delete de la classe mère sinon l'entrée sera vraiment delete!
        self.visible = False
        self.save(reason="Ticket soft deletion.")

    def save(self, *args, **kwargs):
        reason = kwargs.pop('reason', None)

        if not self.ticket_code:
            self.ticket_code = self.__generateTicketCode()
            if reason is None:
                reason = _("Creating new ticket")

        if self.image_folder_name == "":
            self.createTicketImageFolder()

        if self.fk_priority_id is None:
            self.fk_priority_id = self.fk_category.fk_priority_id

        super(Ticket, self).save(*args, **kwargs)

        th = TicketHistory()
        th.fk_manager = self.fk_manager
        th.fk_ticket = self
        th.fk_ticket_status_id = self.fk_status_id
        if reason is not None:
            th.update_reason = reason
        th.save()

    def createTicketImageFolder(self):
        newFolderName = "{}{}".format(settings.MY_ANDROID_PICTURES_PATH, self.ticket_code)
        os.makedirs(newFolderName, exist_ok=True)
        self.image_folder_name = newFolderName


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
        """
        Compte le nombre de bâtiments sans ticket.
        """
        return len(Ticket.objects.filter(fk_building__exact=None))

    def __countAmountOfTicketsForBuilding(self):
        """
        Compte le nombre de tickets pour le bâtiment donné
        """
        return len(Ticket.objects.filter(fk_building__exact=self.fk_building.pk))

    def getTicketHistory(self):
        """
        Retourne l'historique du ticket en cours
        """
        return TicketHistory.objects.filter(fk_ticket=self)

    def getAllTicketComments(self):
        """
        Retourne l'entièreté des commentaires liés à ce ticket
        """
        return TicketComment.objects.filter(fk_ticket=self).order_by("-date_created")

    def setTicketManager(self, manager):
        """
        Change le gestionnaire de ce ticket
        """
        self.fk_manager = manager
        self.save(reason=_("Assigned to manager: {}".format(manager.get_full_name())))
        return self

    def releaseTicketManagement(self):
        """
        Enlève la gestion du ticket de son manager
        """
        self.fk_manager = None
        self.save(reason=_("Manager released ticket management."))
        return self

    def changeTicketStatus(self, targetStatus):
        """
        Change le statut courant du ticket
        """
        self.fk_status = targetStatus
        self.save(reason=_("Ticket status changed to {}".format(targetStatus.label)))
        return self

    def createComment(self, commenter, message):
        """
        Crée un nouveau commentaire pour ce ticket
        """
        newComment = TicketComment()
        newComment.comment = message
        newComment.fk_commenter = commenter
        newComment.fk_ticket = self
        newComment.save(_("A comment has been posted."))
        return newComment

    def getAllSuitableCompanies(self):
        """
        Récupère une liste d'entreprises susceptibles de pouvoir résoudre le problème de ce ticket, en fonction de
            la catégorie et sous-catégorie du ticket.
        La sélection est ensuite triée par distance par rapport au bâtiment lié à ce ticket, s'il y en a un, sinon l'ordre est aléatoire.
        """
        result = list()
        unavailableAddressWeight = 99999
        geopy = GeoPyInterface()

        # Pré sélection des entreprises en fonction de la sous-catégorie
        preselection_subcat = Company.objects.filter(fk_suitableEventCategories__exact=self.fk_category)

        # Ensuite filtrer les entreprises en fonction de la distance en utilisant geopy
        for company in preselection_subcat.all():
            if self.fk_building is not None:
                if company.address is None:
                    result.append((company, unavailableAddressWeight))
                else:
                    companyAddress = "{} {} {} {}".format(company.address, company.city, company.postcode, company.country)
                    ticketAddress = "{} {} {} {}".format(self.fk_building.address, self.fk_building.city, self.fk_building.postcode,
                                                      self.fk_building.country)
                    companyCoords = geopy.findLocationByAddress(companyAddress)
                    ticketCoords = geopy.findLocationByAddress(ticketAddress)
                    if companyCoords["result"] == ResultType.OK and ticketCoords["result"] == ResultType.OK:
                        distanceInKM = geopy.getDistanceBetweenTwoCoordinates(
                            ticketCoords["location"].latitude,
                            ticketCoords["location"].longitude,
                            companyCoords["location"].latitude,
                            companyCoords["location"].longitude)
                        result.append((company, distanceInKM))
                    else:
                        result.append((company, unavailableAddressWeight))
            else:
                result.append((company, unavailableAddressWeight))

        return self.__sortSuitableCompaniesList(result)

    def __sortSuitableCompaniesList(self, list):
        return sorted(list, key=lambda x: x[1])  # On classe la liste par

    def changeCompanyAssignment(self, company_id):
        """
        Modifie la compagnie assignée à la gestion du problème lié à ce ticket
        """
        if company_id == "None":
            self.fk_company = None
        else:
            self.fk_company_id = company_id

        if company_id != "None":
            reason = _("Assigned a new company to the ticket.")
        else:
            reason = _("Unassigned company from this ticket.")
        self.save(reason=reason)
        return self

    def __str__(self):
        ret = "Ticket " + self.ticket_code + " created by " + self.fk_reporter.get_full_name()
        if self.fk_manager is not None:
            ret += " managed by " + self.fk_manager.get_full_name()
        else:
            ret += ", not managed by anyone."
        return ret


class TicketHistory(models.Model):
    """
    Représente l'historique ticket dans lequel chaque opération sur un ticket est enregistrée, avec une raison.
    """
    fk_ticket = models.ForeignKey(Ticket, null=False, blank=False, on_delete=models.CASCADE)
    fk_ticket_status = models.ForeignKey(TicketStatus, null=False, blank=False)
    fk_manager = models.ForeignKey(TicketsUser, verbose_name=_("Who changed the status"), null=True,
                                   blank=True)

    update_date = models.DateTimeField(verbose_name=_("Updated on..."), blank=True, null=False, auto_now_add=True)
    update_reason = models.CharField(verbose_name=_("Update reason"), max_length=200, blank=True, null=False,
                                     default=_("No reason given."))

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
