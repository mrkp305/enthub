from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin

from .managers import UserManager

class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), max_length=254, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
    
    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name