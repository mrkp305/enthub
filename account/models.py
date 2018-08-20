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

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'User Profiles'

    def facebook(self):
        if self.social.facebook is not None:
            return True
    
    def instagram(self):
        if self.social.instagram is not None:
            return True
    
    def twitter(self):
        if self.social.twitter is not None:
            return True
    
    def google(self):
        if self.social.google is not None:
            return True
    

class Social(models.Model):
    profile = models.OneToOneField("account.Profile", related_name='social', verbose_name=_("Person"), on_delete=models.CASCADE)
    twitter = models.CharField(_("Twitter Profile"), blank=True, null=True, max_length=70)
    facebook = models.CharField(_("Facebook Profile"), blank=True, null=True, max_length=70)
    instagram = models.CharField(_("Instagram Profile"), blank=True, null=True, max_length=70)
    google = models.CharField(_("Google Plus Profile"), blank=True, null=True, max_length=70)

    def __str__(self):
        return "Social Media Links for {}".format(self.profile.user)
    
    class Meta:
        verbose_name = 'Social'
        verbose_name_plural = 'Social Media Links'