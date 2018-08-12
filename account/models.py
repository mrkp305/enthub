from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import FileSystemStorage
import uuid
import os
from django.conf import settings

class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

def user_directory_path(instance, filename):
    
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return 'avatar/{}/{}'.format(instance.user.id, filename)

class Profile(models.Model):

    user = models.OneToOneField('authentication.User', verbose_name=_("Credentials"), on_delete=models.CASCADE)
    handle = models.CharField("Unique username", blank=True, unique=True, null=True, max_length=20)
    city = models.ForeignKey("utils.City", blank=True, null=True, on_delete=models.SET_NULL)
    phone = models.CharField("User phone number", blank=True, null=True, max_length=15)
    email_confirmed = models.BooleanField("Confirmation status", default=False)
    tags = models.ManyToManyField("utils.Tag", related_name='users', blank=True, verbose_name=_("User tags"))
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(_("Profile Picture"),storage=OverwriteStorage(),blank=True, null=True, upload_to=user_directory_path, height_field=None, width_field=None, max_length=None)

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)
