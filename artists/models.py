'''
    Django Imports
'''

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import FileSystemStorage
from django.conf import settings

'''
    End Django Imports
'''


'''
    Python Imports
'''

import os
import uuid

'''
    End Python Imports
'''


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return 'artist/{}/{}'.format(instance.user.id, filename)


class Artist(models.Model):
    user_profile = models.OneToOneField("account.Profile", verbose_name=_("User Profile"), on_delete=models.CASCADE)
    stage_name = models.CharField(_("Stage name"), max_length=50)
    genre = models.ForeignKey('utils.Genre', related_name='artist_genre', blank=True, null=True, on_delete=models.SET_NULL)
    alias = models.CharField(_("aka"), blank=True, null=True, max_length=50)
    bio = models.TextField(_("Artist Bio"))
    dob = models.DateField(_("Artist's date of birth"), blank=True, null=True, auto_now=False, auto_now_add=False)
    use_profile_avatar = models.BooleanField(_("Use profile picture as artist profile picture too"), default=True)

    class Meta:
        verbose_name = 'Artist Profile'
        verbose_name_plural = 'Artists'
    
    def __str__(self):
        return self.stage_name
    
class Contact(models.Model):
    artist = models.ForeignKey("artists.Artist", related_name='contacts', verbose_name=_("Artist"), on_delete=models.CASCADE)
    person = models.CharField(_("Contact Person"), max_length=50)
    purpose = models.CharField(_("Purpose Of The Contact"), max_length=50)
    phone = models.CharField(_("Contact Person's Phone"), max_length=50)
    email = models.EmailField(_("Contact Person's Email Address"), max_length=254, blank=True, null=True)
    last_updated = models.DateTimeField(_("Last Updated On"), auto_now=True)
    
    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Artist Contacts'
    
    def __str__(self):
        return "Contact info for : {}".format(self.artist)