from django.db import models
from django.utils.translation import ugettext_lazy as _

class Profile(models.Model):
    user = models.ForeignKey('authentication.User', verbose_name=_("Credentials"), on_delete=models.CASCADE)
