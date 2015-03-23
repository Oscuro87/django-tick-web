from django.forms import ModelChoiceField
from simplemathcaptcha.fields import MathCaptchaField
from django import forms
from django.utils.translation import ugettext as _
from django_countries.widgets import CountrySelectWidget
from login.models import TicketsUserManager
from ticketing.models import CompanyManager, BuildingManager
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

class TicketAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tum = TicketsUserManager()
        bm = BuildingManager()
        compMan = CompanyManager()
        self.fields['fk_manager'].queryset = tum.get_managers_only()
        mcf = self.fields['fk_building']
        assert isinstance(mcf, ModelChoiceField)
        #self.fields['fk_reporter'].queryset = bm.get_users_for_building(self.fields['fk_building'])
        self.fields['fk_company'].queryset = compMan.get_companies_for_event_category(self.fields['fk_category'].queryset.last())