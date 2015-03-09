from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, GroupManager


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

    def get_managers_only(self):
        findgroup = ["Manager", "Root"]
        return TicketsUser.objects.filter(groups__name__in=findgroup)

    def get_users_for_building_id(self, building_id=None):
        if building_id is None:
            return TicketsUser.objects.filter(groups__name__exact="User")
        else:
            return TicketsUser.objects.filter(groups__name__exact="User")#TODO

"""
Cette classe représente soit un utilisateur "lambda", soit un membre du staff (gestionnaire de ticket, admin, ...)
"""
class TicketsUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    objects = TicketsUserManager()
    first_name = models.CharField(_('first name'), max_length=30, blank=False, null=False, default="")
    last_name = models.CharField(_('last name'), max_length=30, blank=False, null=False, default="")
    email = models.EmailField(_('email address'), max_length=255, null=False, blank=False, default="", unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_(
                                        'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    receive_newsletter = models.BooleanField(_('receive newsletter'), default=False)

    USERNAME_FIELD = 'email'

    def save(self, *args, **kwargs):
        if not self.password.__contains__("sha256$"):
            self.set_password(self.password)
        super(TicketsUser, self).save(*args, **kwargs)

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
        return True if (g_name=="Manager" or g_name=="Administrator" or g_name=="Root") else False

    def __str__(self):
        try:
            group_name = self.groups.values_list('name', flat=True)[0]
            return group_name + ": " + self.get_full_name() + " (" + self.email + ")"
        except IndexError:
            return "Ungrouped!: " + self.get_full_name() + " (" + self.email + ")"
