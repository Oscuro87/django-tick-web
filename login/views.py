from django.shortcuts import render_to_response, RequestContext, redirect
from django.views.generic import TemplateView
from login.forms import LoginForm
from django.contrib import auth
from django.contrib import messages
from django.utils.translation import ugettext as _

class LoginView(TemplateView):
    template_name = "login/login.html"

    # Custom vars
    __gravities = ("danger", "info", "success")
    __user_feedback = []

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('homeview')

        return self.showPlainLoginView()

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('homeview')

        if "loginGo" in request.POST:
            return self.processLogin()

        return self.showPlainLoginView()

    def showPlainLoginView(self):
        data = dict()
        loginForm = LoginForm()

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
