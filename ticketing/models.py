from django.db import models
from django.utils.translation import ugettext as _

from login.models import TicketsUser


class TicketStatus(models.Model):
    label = models.CharField(verbose_name=_("Status"), max_length=64, null=False, blank=False)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name_plural = _("Ticket statuses")


class TicketPriority(models.Model):
    label = models.CharField(verbose_name=_("Priority"), max_length=64, null=False, blank=False)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name_plural = _("Ticket priorities")


class Channel(models.Model):
    label = models.CharField(verbose_name=_("Way of ticket creation"), max_length=64, null=False, blank=False)

    def __str__(self):
        return self.label


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
        ordering = ["building_name",]


class Place(models.Model):
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
    address = models.CharField(verbose_name=_("Street"), max_length=45, blank=False, null=False, unique=True)
    vicinity = models.CharField(verbose_name=_("Vicinity name"), max_length=45, blank=False, null=False, default="")
    postcode = models.IntegerField(verbose_name=_("Postcode"), null=False, blank=False, default="0")
    phone_number = models.CharField(verbose_name=_("Telephone number"), max_length=45, blank=True, null=True, default="")
    name = models.CharField(verbose_name=_("Company name"), max_length=45, null=False, blank=False)
    vat_number = models.CharField(verbose_name=_("VAT Number"), max_length=45, null=False, blank=False, unique=True)
    visible = models.BooleanField(verbose_name=_("Is visible?"), null=False, blank=False, default=True)

    def __str__(self):
        return self.name + " (" + self.vat_number + ")"

    class Meta:
        verbose_name_plural = "Companies"


class EventCategory(models.Model):
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


class TicketManager(models.Manager):
    def all(self):
        return super(TicketManager, self).get_queryset()

    def create_ticket(self, batimentID, subcategoryID, creatorID, channelID, statusID, priorityID, floor, office, description):
        t = Ticket()
        t.fk_building_id = batimentID
        t.fk_category_id = subcategoryID
        t.fk_renter_id = creatorID
        t.fk_channel_id = channelID
        t.fk_status_id = statusID
        t.fk_priority_id = priorityID
        t.floor = floor
        t.office = office
        t.description = description
        t.save()

        newHistory = TicketHistory()
        newHistory.fk_ticket = self
        newHistory.fk_ticket_status = self.fk_status
        newHistory.fk_manager = self.fk_manager
        newHistory.update_reason = _("Ticket creation.")
        newHistory.save()

        return True


class Ticket(models.Model):
    objects = TicketManager()
    fk_building = models.ForeignKey(Building, verbose_name=_("Building"), null=False, blank=False)
    fk_channel = models.ForeignKey(Channel, verbose_name=_("Channel"), null=False, blank=False)
    fk_category = models.ForeignKey(EventCategory, verbose_name=_("Category"), null=False, blank=False)
    fk_renter = models.ForeignKey(TicketsUser, verbose_name=_("Renter"), related_name="locataire", null=False, blank=False)
    fk_priority = models.ForeignKey(TicketPriority, verbose_name=_("Priority"), null=False, blank=False)
    fk_status = models.ForeignKey(TicketStatus, verbose_name=_("Status"), null=False, blank=False)  # TODO: default=1

    ticket_code = models.CharField(verbose_name=_("Ticket code"), max_length=10, null=False, blank=True, unique=True)
    fk_manager = models.ForeignKey(TicketsUser, verbose_name=_("Manager"), related_name="gestionnaire", null=True, blank=True)
    fk_company = models.ForeignKey(Company, verbose_name=_("Company"), null=True, blank=True)
    floor = models.CharField(max_length=45, null=True, blank=True, default="")
    office = models.CharField(max_length=45, null=True, blank=True, default="")
    visible = models.BooleanField(verbose_name=_("Is visible?"), null=False, blank=False, default=True)
    intervention_date = models.DateField(verbose_name=_("Date of intervention"), null=True, blank=True, default=None)
    description = models.TextField(verbose_name=_("Event description"), null=True, blank=True,
                                  default=_("No description available."))



    def save(self, *args, **kwargs):
        if not self.ticket_code:
            self.ticket_code = self.generateTicketCode()

        super(Ticket, self).save(*args, **kwargs)

    def generateTicketCode(self):
        count = self.countAmountOfTickets() + 1
        code = self.fk_building.building_code + "-" + str(count)
        print(code)
        return code

    def countAmountOfTickets(self):
        return len(Ticket.objects.filter(fk_building__exact=self.fk_building.pk))

    def getAllHistory(self):
        return TicketHistory.objects.filter(fk_ticket=self)

    def __str__(self):
        ret = "Ticket " + self.ticket_code + " created by " + self.fk_renter.get_full_name()
        if self.fk_manager is not None:
            ret += " managed by " + self.fk_manager.get_full_name()
        else:
            ret += ", not managed by anyone."
        return ret

class TicketHistory(models.Model):
    update_date = models.DateTimeField(verbose_name=_("Updated on..."), blank=True, null=False, auto_now_add=True)
    update_reason = models.CharField(verbose_name=_("Update reason"), max_length=200, blank=True, null=False, default=_("No reason given."))
    fk_ticket = models.ForeignKey(Ticket, null=False, blank=False, on_delete=models.CASCADE)
    fk_ticket_status = models.ForeignKey(TicketStatus, null=False, blank=False)
    fk_manager = models.ForeignKey(TicketsUser, verbose_name=_("Who changed the status"), null=True,
                                           blank=True)

    class Meta:
        verbose_name_plural = "Ticket histories"

    def __str__(self):
        return "" + self.fk_ticket.ticket_code + " changed to " + self.fk_ticket_status.label + " on " + str(self.update_date)


class Language(models.Model):
    language_name = models.CharField(max_length=50, blank=False, null=False, default="English")
    language_code = models.CharField(max_length=5, blank=False, null=False, default="en-us")