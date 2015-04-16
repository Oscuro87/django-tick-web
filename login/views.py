from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.shortcuts import render_to_response, RequestContext, redirect
from django.views.generic import TemplateView
from login.forms import LoginForm
from django.contrib import auth
from django.contrib import messages
from django.utils.translation import ugettext as _
from login.models import TicketsUser
from ticketing.forms import RegistrationForm
from tickets import settings


class LoginView(TemplateView):
    template_name = "login/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('homeview')

        return self.showPlainLoginView()

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('homeview')

        if "loginGo" in request.POST:
            return self.processLogin()

        if "goToRegister" in request.POST:
            return redirect("register-view")

        return self.showPlainLoginView()

    def showPlainLoginView(self):
        data = dict()
        loginForm = LoginForm()

        data['registrationActive'] = settings.MY_REGISTRATION_ENABLED
        data['user_feedback'] = []
        data['loginform'] = loginForm

        return render_to_response(self.template_name, data, RequestContext(self.request))

    def processLogin(self):
        form = LoginForm(data=self.request.POST)

        if form.is_valid():
            user = auth.authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    auth.login(self.request, user)
                    self.request.session['show_unrelated_tickets'] = False
                    messages.add_message(self.request, messages.SUCCESS, _("Successfully logged in."))
                    return redirect('homeview')
                else:
                    messages.add_message(self.request, messages.ERROR, _("This user is banned."))
            else:
                messages.add_message(self.request, messages.ERROR, _("You entered the wrong credentials, please try again."))
        else:
            messages.add_message(self.request, messages.ERROR, _("Please fill the form correctly."))

        return redirect('loginview')


class RegisterView(TemplateView):
    template_name = "login/register.html"

    def post(self, request, *args, **kwargs):
        if "cancelRegistration" in request.POST:
            return redirect("loginview")

        if "sendRegistration" in request.POST:
            return self.processRegistration()

        return self.show()

    def get(self, request, *args, **kwargs):
        return self.show()

    def processRegistration(self):
        # Groupe par défaut pour les nouveaux arrivants, modifiable par les admins!
        retrieve = RegistrationForm(self.request.POST)
        if retrieve.is_valid():
            newUser = TicketsUser()
            newUser.email = retrieve.cleaned_data['email']
            newUser.password = retrieve.cleaned_data['password']
            newUser.first_name = retrieve.cleaned_data['first_name']
            newUser.last_name = retrieve.cleaned_data['last_name']
            newUser.phone_number = retrieve.cleaned_data['phone_number']
            newUser.save()

            messages.success(self.request, _("Registration successful! (Redirected to the login screen)"))

            return redirect('loginview')
        else:
            errors = retrieve.errors.as_data()
            message = _("Registration failed:\n")
            for key, value in errors.items():
                valErr = value[0]
                message = message + key + ": " + valErr.__str__() + "\n"
            messages.error(self.request, message)

        print("TODO processRegistration")
        return self.show()

    def show(self):
        regForm = RegistrationForm()

        data = {}

        data["registrationForm"] = regForm

        return render_to_response(self.template_name, data, RequestContext(self.request))
