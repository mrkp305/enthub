from django.db import models
from django.utils.translation import ugettext_lazy as _

class Profile(models.Model):
    user = models.OneToOneField('authentication.User', verbose_name=_("Credentials"), on_delete=models.CASCADE)
    handle = models.CharField("Unique username", blank=True, unique=True, null=True, max_length=20)
    city = models.ForeignKey("utils.City", blank=True, null=True, on_delete=models.SET_NULL)
    phone = models.CharField("User phone number", blank=True, null=True, max_length=15)
    email_confirmed = models.BooleanField("Confirmation status", default=False)
    tags = models.ManyToManyField("utils.Tag", related_name='users', blank=True, verbose_name=_("User tags"))
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

    
    