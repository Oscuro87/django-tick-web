from django.forms import ModelChoiceField
from simplemathcaptcha.fields import MathCaptchaField
from django import forms
from django.utils.translation import ugettext as _
from django_countries.widgets import CountrySelectWidget
from login.models import TicketsUserManager, TicketsUser
from ticketing.models import CompanyManager, BuildingManager, EventCategory, Company
from ticketing.models import Building


class ContactForm(forms.Form):
    # Email field is read only & pre filled
    subject = forms.CharField(max_length=128, min_length=5, required=True, label=_("Subject: "))
    content = forms.CharField(max_length=500, min_length=5, required=True, label=_("Your message: "))
    captcha = MathCaptchaField()

    widgets = {"content": forms.TextInput}


class TicketCommentForm(forms.Form):
    comment_field = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 60}), min_length=3, max_length=300,
                                    required=True, label=_('Your comment'))


class BuildingCreationForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ('country', 'address', 'city', 'vicinity', 'postcode', 'building_name')
        widgets = {'country': CountrySelectWidget}
        required = ('country', 'address', 'city', 'postcode', 'building_name')
        labels = {
            'country': _('Country'),
            'address': _('Address'),
            'city': _('City'),
            'vicinity': _('Vicinity name'),
            'postcode': _('Postcode'),
            'building_name': _('Name of the building'),
        }


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = TicketsUser
        fields=['email', 'password', 'first_name', 'last_name', 'phone_number']
        required=['email', 'password', 'first_name', 'last_name']
        widgets = {'password': forms.PasswordInput}


class CompanyUpdateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'address', 'vicinity', 'postcode', 'city', 'country',
                   'phone_number', 'vat_number', 'fk_suitableEventCategories']
        required = ['fk_suitableEventCategories', 'country', 'address', 'city', 'postcode', 'phone_number', 'name']
        widgets = {'fk_suitableEventCategories': forms.SelectMultiple}
        labels = {
            'fk_suitableEventCategories': _("Suitable event categories (hold CTRL and click to select multiple options)"),
            'country': _("Country"),
            'address': _("Address"),
            'vicinity': _("Vicinity"),
            'city': _("City"),
            'postcode': _("Postcode"),
            'phone_number': _("Phone number"),
            'name': _("Name"),
            'vat_number': _("VAT number"),
        }


############### Admin forms ######################
class TicketAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tum = TicketsUserManager()
        bm = BuildingManager()
        compMan = CompanyManager()
        self.fields['fk_manager'].queryset = tum.getManagersOnly()
        #self.fields['fk_reporter'].queryset = bm.get_users_for_building(self.fields['fk_building'])


class EventCategoryAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fk_parent_category'].queryset = EventCategory.objects.filter(fk_parent_category=None)
