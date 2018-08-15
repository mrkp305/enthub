from django.db import models
from django.utils.translation import ugettext_lazy as _

class Event(models.Model):
    name = models.CharField(verbose_name="Event Title", max_length=255)
    type = models.ForeignKey("utils.EventType", verbose_name=_("Event type"), blank=True, null=True, on_delete=models.SET_NULL)
    about = models.TextField(verbose_name="About Event", blank=True, null=True)
    recurring = models.BooleanField(verbose_name="Is Recurring", default=False)
    start_date = models.DateTimeField(verbose_name="Start Date", auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField(verbose_name="End Date", auto_now=False, auto_now_add=False)
    added_by = models.ForeignKey("authentication.User", verbose_name=_("Added By"), blank=True, null=True, on_delete=models.SET_NULL)
    website = models.URLField(verbose_name="Website",blank=True, null=True, max_length=200)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
    
    def __str__(self):
            return self.name

class Contact(models.Model):
    event = models.ForeignKey("events.Event", verbose_name=_("Event"), on_delete=models.CASCADE)
    person = models.CharField(verbose_name="Contact Person", max_length=50, blank=True, null=True)
    phone = models.CharField(verbose_name="Phone Number", max_length=15)
    email = models.EmailField(verbose_name="Email Address",blank=True, null=True, max_length=254)
    whatsapp = models.BooleanField(verbose_name="Is on WhatsApp", default=False)

    class Meta:
        verbose_name = 'Event contact'
        verbose_name_plural = 'Event contacts'
    
    def __str__(self):
            return self.phone
