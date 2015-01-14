from django import forms
from django.utils.translation import ugettext as _


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, min_length=5, required=True, label=_("Email: "))
    password = forms.CharField(widget=forms.PasswordInput, max_length=32, required=True, label=_("Password: "))
    
