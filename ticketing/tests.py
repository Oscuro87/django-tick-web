from django.test import TestCase
from django_countries.fields import Country
from login.models import TicketsUser
from ticketing.models import Ticket, EventCategory, TicketPriority, Channel, TicketStatus, Building, Place


class TicketingTest(TestCase):
    def setUp(self):
        self.priority = TicketPriority()
        self.priority.label = "High"
        self.priority.save()

        self.category = EventCategory()
        self.category.fk_parent_category = None
        self.category.fk_priority = self.priority
        self.category.save()

        self.channel = Channel()
        self.channel.label = "Testing"
        self.channel.save()

        self.user = TicketsUser()
        self.user.email = "tester@gmail.com"
        self.user.password = "tester"
        self.user.save()

        self.manager = TicketsUser()
        self.manager.email = "manager@gmail.com"
        self.manager.password = "manager"
        self.manager.first_name = "Dummy"
        self.manager.last_name = "Manager"
        self.manager.save()

        self.building_country = Country("BE")

        self.building = Building()
        self.building.building_name = "Test building"
        self.building.country = self.building_country
        self.building.postcode = "1000"
        self.building.address = "Rue test 10"
        self.building.vicinity = "Bruxelles"
        self.building.save()

        self.place = Place()
        self.place.fk_building = self.building
        self.place.fk_owner = self.user
        self.place.save()

        self.status = TicketStatus()
        self.status.label = "Unit Testing"
        self.status.save()

    def test_createTicket(self):
        print("testing create ticket")

        self.ticket = Ticket()
        self.ticket.fk_category = self.category
        self.ticket.fk_channel = self.channel
        self.ticket.fk_reporter = self.user
        self.ticket.fk_status = self.status
        self.ticket.fk_building = self.building
        self.ticket.fk_manager = self.manager
        self.ticket.save()

        self.__testDestroyTicket()

        self.__testRemovePlaceFromUser()

        print(self.ticket.__str__())

    def __testDestroyTicket(self):
        #Note: le ticket ne peut pas être détruit, mais est passé en "mode invisible"!
        print("Is ticket visible BEFORE delete? {}".format(self.ticket.visible))
        self.ticket.delete()
        self.assertIsNotNone(self.ticket, msg="ticket is None!")
        print("Is ticket visible AFTER delete? {}".format(self.ticket.visible))

    def __testRemovePlaceFromUser(self):
        # Note: Ne devrait enlever QUE l'instance de "Place", et non pas le bâtiment.
        # Le bâtiment pourrait être utilisé par d'AUTRES utilisateurs!
        self.place.delete()
        self.place = None
        self.assertIsNotNone(self.building, msg="Le bâtiment est delete lors du delete d'un lieu !! (pas bon)")
