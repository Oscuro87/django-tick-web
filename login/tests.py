from django.test import TestCase, RequestFactory
from login.models import TicketsUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib import auth


class LoginTest(TestCase):
    __test_email = "testuser@gmail.com"
    __test_pass = "cornholio"
    __test_first_name = "Corn"
    __test_last_name = "Holio"
    __test_user_object = None
    __test_user_session = None
    __request_factory = RequestFactory()

    def setUp(self):
        # Create temporary test accounts
        try:
            self.__test_user_object = TicketsUser.objects.get(email=self.__test_email)
        except TicketsUser.DoesNotExist:
            self.__test_user_object = TicketsUser.objects.create_user(email=self.__test_email,
                                                                      password=self.__test_pass)
            assert isinstance(self.__test_user_object, TicketsUser)
            self.__test_user_object.first_name = self.__test_first_name
            self.__test_user_object.last_name = self.__test_last_name

    def __addSessionToRequest(self, request):
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

    def __doLogin(self):
        assert isinstance(self.__test_user_object, TicketsUser)

        crafted_request = self.__request_factory.post(path='', data={'email': self.__test_email, 'password': self.__test_pass})
        self.__addSessionToRequest(crafted_request)

        self.__test_user_object = auth.authenticate(email=crafted_request.POST.get('email'), password=crafted_request.POST.get('password'))
        auth.login(crafted_request, self.__test_user_object)

    def test_user_exists(self):
        self.assertTrue((self.__test_user_object is not None), "The test user exists.")

    def test_can_login(self):
        self.__doLogin()
        self.assertTrue((self.__test_user_object.is_authenticated()), "User authenticated, ready for login.")

    def test_name(self):
        self.assertTrue(self.__test_user_object.get_short_name()==self.__test_first_name)
        self.assertTrue(self.__test_user_object.get_last_name()==self.__test_last_name)
        self.assertTrue(self.__test_user_object.get_full_name()==self.__test_first_name + " " + self.__test_last_name)

    def test_permission_ungrouped(self):
        self.assertTrue(self.__test_user_object.get_group_name()==None)
