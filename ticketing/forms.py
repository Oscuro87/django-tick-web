from simplemathcaptcha.fields import MathCaptchaField
from django import forms
from django.utils.translation import ugettext as _
from django_countries.widgets import CountrySelectWidget
from ticketing.models import Building


class ContactForm(forms.Form):
    # Email field is read only & pre filled
    subject = forms.CharField(max_length=128, min_length=3, required=True, label=_("Subject: "))
    content = forms.CharField(max_length=500, min_length=3, required=True, label=_("Your message: "))
    captcha = MathCaptchaField()


class TicketCommentForm(forms.Form):
    comment_field = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 60}), min_length=3, max_length=300,
                                    required=True, label=_('Your comment'))


class BuildingCreationForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ('country', 'address', 'vicinity', 'postcode', 'building_name')
        widgets = {'country': CountrySelectWidget}
        required = ('country', 'address', 'postcode', 'building_name')
        labels = {
            'country': _('Country'),
            'address': _('Address'),
            'vicinity': _('Vicinity name'),
            'postcode': _('Postcode'),
            'building_name': _('Name of the building'),
        }