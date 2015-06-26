from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager
from common.models import AbstractBaseModel
from music.models import Instrument


class User(AbstractBaseUser, PermissionsMixin):
    """
    User class implements a fully featured User model with
    admin-compliant permissions.

    First/last names, password and email are required. Other fields are optional.
    """
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Member(AbstractBaseModel):
    pass


class BoardMember(Member):
    pass


class Director(Member):
    pass


class Musician(Member):
    primary_instrument = models.ForeignKey(Instrument, related_name='primary_musicians')
    other_instruments = models.ManyToManyField(Instrument, related_name='other_musicians')


class StaffMember(Member):
    pass


class Role(AbstractBaseModel):
    name = models.CharField(max_length=100, unique=True)