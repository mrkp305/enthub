from django.db import models
from django.utils.translation import ugettext_lazy as _
import uuid
from django.conf import settings
from datetime import datetime

class Event(models.Model):
    name = models.CharField(verbose_name="Event Title", max_length=255)
    type = models.ForeignKey("utils.EventType", verbose_name=_("Event type"), blank=True, null=True, on_delete=models.SET_NULL)
    about = models.TextField(verbose_name="About Event", blank=True, null=True)
    recurring = models.BooleanField(verbose_name="Is Recurring", default=False)
    start_date = models.DateTimeField(verbose_name="Start Date", auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField(verbose_name="End Date", auto_now=False, auto_now_add=False)
    added_by = models.ForeignKey("authentication.User", verbose_name=_("Added By"), blank=True, null=True, on_delete=models.SET_NULL)
    website = models.URLField(verbose_name="Website",blank=True, null=True, max_length=200)
    admission = models.TextField(_("Admission"), blank=True, null=True)
    location = models.ForeignKey("events.Location", verbose_name=_("Location"),blank=True, null=True, on_delete=models.SET_NULL)
    paid_for = models.BooleanField(_("Paid for"), default=False)
    verified = models.BooleanField(_("Accepted by Moderator"), default=False)
    created_at= models.DateTimeField(_("Last Updated On"), auto_now_add=True)
    last_modified = models.DateTimeField(_("Last Updated On"), auto_now=True)
    

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
    
    def __str__(self):
            return self.name

    def get_poster_url(self):
        return self.poster_set.filter(main=True)[0].image.url

    def get_address(self):
        if self.location.street_address is not None:
            if len(self.location.street_address) > 22:
                return "{}, {}-{}".format(self.location.street_address[:22],self.location.city, self.location.city.country.iso_code2)
            else:
                return "{}, {}".format(self.location.street_address,self.location.city.name)

    def poster_count(self):
        return self.poster_set.count()
    
    def get_other_posters(self):
        return self.poster_set.all()
    
    def time_since_added(self):
        then = self.created_at.replace(tzinfo=None)
        now = datetime.now().replace(tzinfo=None)

        duration = now - then
        seconds_since = duration.total_seconds()

        days_since =duration.days
        days  = divmod(seconds_since, 86400)[0]
        hours = divmod(seconds_since, 3600)[0]
        minutes = divmod(seconds_since, 60)[0]
        seconds = duration.seconds

        if days <= 0:
            if minutes < 60:
                if minutes < 1:
                    return "{}s ago.".format(str(seconds).split('.')[0])
                else:
                    return "{}m ago.".format(str(minutes).split('.')[0])
            else:
                return "{}h ago.".format(str(hours).split('.')[0])
        else:
            if days == 1:
                return "{}d ago.".format(str(days).split('.')[0])
            elif days > 7:
                if days <= 30:
                    weeks = days//7
                    return "{}w ago.".format(str(weeks).split('.')[0])
                elif days <= 365:
                    months = days//30
                    return "{}mo ago.".format(str(months).split('.')[0])
                else:
                    years = days//365
                    return "{}y ago.".format(str(years).split('.')[0])





class Location(models.Model):
    name = models.CharField(_("Location name"), max_length=50)
    street_address = models.CharField(_("Street address"),blank=True, null=True, max_length=50)
    zip_code = models.CharField(_("Zip code"),blank=True, null=True, max_length=50)
    latitude = models.CharField(_("Latitude"),blank=True, null=True, max_length=50)
    longitude = models.CharField(_("Longitude"),blank=True, null=True, max_length=50)
    city = models.ForeignKey("utils.City", verbose_name=_(""), blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Event Location'
        verbose_name_plural = 'Event Locations'

    def __str__(self):
        return self.name


class Contact(models.Model):
    event = models.ForeignKey("events.Event", verbose_name=_("Event"), on_delete=models.CASCADE)
    person = models.CharField(verbose_name="Contact Person", max_length=50, blank=True, null=True)
    phone = models.CharField(verbose_name="Phone Number", max_length=15)
    email = models.EmailField(verbose_name="Email Address",blank=True, null=True, max_length=254)
    whatsapp = models.BooleanField(verbose_name="Is on WhatsApp", default=False)
    created_at= models.DateTimeField(_("Last Updated On"), auto_now_add=True)
    last_modified = models.DateTimeField(_("Last Updated On"), auto_now=True)

    class Meta:
        verbose_name = 'Event contact'
        verbose_name_plural = 'Event contacts'
    
    def __str__(self):
        return self.phone

def directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return 'events/posters/{}'.format(filename)

class Poster(models.Model):
    event = models.ForeignKey("events.Event", verbose_name=_("Event"), on_delete=models.CASCADE)
    image = models.ImageField(_("Poster"), upload_to=directory_path, height_field=None, width_field=None, max_length=None)
    main = models.BooleanField(_("Is Main"), default=False)

    def __str__(self):
            return "Poster for '{}'".format(self.event)

    class Meta:
        verbose_name = 'poster'
        verbose_name_plural = 'Posters'