from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group


class TicketsUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError(_('The given email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=False,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True,
                                 **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user

    def getManagersOnly(self):
        findgroup = ["Manager", "Root"]
        return TicketsUser.objects.filter(groups__name__in=findgroup)

    def sendContactMessageToAdmins(self, messageSubject, messageContent):
        recipients = self.getManagersOnly()
        for person in recipients:
            assert isinstance(person, TicketsUser)
            subject = _("An user has sent a message through the contact form")
            message = _("<p>Message subject: {}</p><p>Content: {}</p>".format(messageSubject, messageContent))
            try:
                send_mail(subject, "", "ticketing.platform@gmail.com", [person.email], fail_silently=False,
                          html_message=message)
            except ConnectionRefusedError as e:
                print("Cannot send email to commenters, connection to email provider is impossible: \n{}".format(
                    e.__str__()))


class TicketsUser(AbstractBaseUser, PermissionsMixin):
    """
    Cette classe représente soit un utilisateur "lambda", soit un membre du staff (gestionnaire de ticket, admin, ...)
    """

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    objects = TicketsUserManager()
    fk_company = models.ForeignKey("ticketing.Company", verbose_name=_("Linked company"), blank=True, null=True, default=None)
    first_name = models.CharField(verbose_name=_('first name'), max_length=30, blank=True, null=True, default="")
    last_name = models.CharField(verbose_name=_('last name'), max_length=30, blank=True, null=True, default="")
    email = models.EmailField(verbose_name=_('email address'), max_length=255, null=False, blank=False, default="",
                              unique=True)
    is_staff = models.BooleanField(verbose_name=_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(verbose_name=_('active'), default=True,
                                    help_text=_(
                                        'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(verbose_name=_('date joined'), default=timezone.now)
    phone_number = models.CharField(verbose_name=_("Phone number"), max_length=64, null=True, blank=True)
    receive_newsletter = models.BooleanField(verbose_name=_('receive newsletter'), default=False)

    USERNAME_FIELD = 'email'

    def save(self, *args, **kwargs):
        if not self.password.__contains__("sha256$"):
            self.set_password(self.password)

        super(TicketsUser, self).save(*args, **kwargs)

        print(self.groups.all())
        if len(self.groups.all()) == 0:
            userGroup = Group.objects.get(name='User')
            self.groups.add(userGroup)
            self.save()

    def isUserACompany(self):
        return self.fk_company is not None

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def get_group_name(self):
        try:
            return self.groups.values_list('name', flat=True)[0]
        except IndexError:
            return None

    def isAdmin(self):
        g_name = self.get_group_name()
        return True if (g_name == "Manager" or g_name == "Administrator" or g_name == "Root") else False

    def __str__(self):
        string = "{} ({})".format(self.get_full_name(), self.email)
        if self.isUserACompany():
            string += " (Company Account)"
        return string
