from django.contrib import admin
from .models import Event, Contact, Poster, Location
# Register your models here.
admin.site.register(Event)
admin.site.register(Contact)
admin.site.register(Poster)
admin.site.register(Location)