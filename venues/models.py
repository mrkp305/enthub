from django.db import models
from django.utils.translation import ugettext_lazy as _
import uuid
import os
from django.conf import settings
from django.utils.text import slugify
from django.shortcuts import reverse


class Venue(models.Model):
     
    name = models.CharField( max_length=150)
    suitable = models.ManyToManyField("utils.EventPurpose", verbose_name=_("Suitable for"))
    description = models.TextField(_("Description"))
  
    #contacts
    website = models.URLField()
    contact_person = models.CharField(max_length=60)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    is_on_whatsapp = models.BooleanField(default=True)

    #location
    street_address = models.CharField(max_length=100)
    city = models.ForeignKey("utils.City", verbose_name=_("City"), blank=True, null=True, on_delete=models.SET_NULL) 
    latitude = models.CharField(max_length=30)
    longitude = models.CharField(max_length=30)
    added_by = models.ForeignKey("authentication.User", verbose_name=_("Added by"),blank=True, null=True, on_delete=models.SET_NULL)
    created_at= models.DateTimeField(_("Last Updated On"), auto_now_add=True)
    last_modified = models.DateTimeField(_("Last Updated On"), auto_now=True)

    def get_absolute_url(self):
        return reverse('venues:view-venue', kwargs={'id':self.id, 'slug':slugify(self.name)})

    def get_img_url(self):
        return self.images_set.filter(is_main=True)[0].image.url

    def get_purposes(self):
        return self.suitable.all()

    def poster_count(self):
        return self.images_set.count()
    
    def get_other_posters(self):
        return self.images_set.all()

def directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return 'venues/images/{}'.format(filename)

class Images(models.Model):
    venue = models.ForeignKey("venues.Venue", verbose_name=_("Venue"), on_delete=models.CASCADE)
    image = models.ImageField(_("Venue Image"), upload_to=directory_path, height_field=None, width_field=None, max_length=None)
    is_main = models.BooleanField(_("Is main banner"), default=False)

