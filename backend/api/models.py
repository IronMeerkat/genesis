from datetime import timezone, datetime
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from boilerplate.models import Model, GenesisUserManager
from djongo import models
from django.utils.translation import gettext_lazy as _
from simple_history import register


class User(AbstractBaseUser, PermissionsMixin, Model):

    objects = GenesisUserManager()
    all_objects = GenesisUserManager(alive_only=False)

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=datetime.now)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)


    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

class Message(Model):

    """Relatively generic model with two owners
    """

    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, related_name='sender')
    recepient = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, related_name='recepient')

    timestamp = models.DateTimeField(auto_now=True)

    title = models.CharField(null=False, max_length=64)
    body = models.CharField(null=False, max_length=2048)

    read = models.ArrayReferenceField(to=User, related_name='has_read', null=True)
    deleted = models.ArrayReferenceField(to=User, related_name='has_deleted', null=True)

