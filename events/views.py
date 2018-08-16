'''
    Django Imports
'''

from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, Http404
from django.views import View
from django.views.defaults import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.files.base import ContentFile
from django.contrib import messages
from datetime import *

'''
    End Django Imports
'''


'''
    Form Imports
'''

from .forms import *


'''
    End form imports
'''

'''Model Imports
'''
from .models import *
from utils.models import *
from authentication.models import User


class Events(View):
    def get(self, request):
        pass

class Add(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/auth'
    def test_func(self):
        return True

    def get(self, request):
        template = "main/events/add.html"
        context = {
            'EventForm': EventForm(),
        }
        return HttpResponse(render(request, template, context))

    def post(self, request):
        if 'post_event' in request.POST:
            form = EventForm(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                type = form.cleaned_data.get('type')
                start_date = form.cleaned_data.get('start_date')
                start_time = form.cleaned_data.get('start_time')
                end_date = form.cleaned_data.get('end_date')
                end_time = form.cleaned_data.get('end_time')
                admission = form.cleaned_data.get('admission')
                main_poster = request.FILES['main_poster']

                
                location_name = form.cleaned_data.get('location_name')
                city = form.cleaned_data.get('city')
                street_address = form.cleaned_data.get('street_address')
                zip_code = form.cleaned_data.get('zip_code')
                latitude = form.cleaned_data.get('latitude')
                longitude = form.cleaned_data.get('longitude')

                about = form.cleaned_data.get('about')

                contact_person = form.cleaned_data.get('contact_person')
                phone = form.cleaned_data.get('phone')
                email = form.cleaned_data.get('email')
                website = form.cleaned_data.get('website')
                whatsapp = form.cleaned_data.get('is_on_whatsapp')
                
                #The Location first, since Event Object depends on it
                location = Location.objects.create(
                    name=location_name
                )
                if street_address:
                    location.street_address=street_address
                if city:
                    location.city = City.objects.get(id=city)
                if zip_code:
                    location.zip_code = zip_code
                if latitude:
                    location.latitude = latitude
                if longitude:
                    location.longitude = longitude
                location.save()
                
                #The Event
                event = Event.objects.create(
                    name=title,
                    start_date=datetime.combine(start_date, start_time),
                    end_date=datetime.combine(end_date, end_time),
                    added_by=User.objects.get(id=request.user.id),
                    location=location
                )
               
                if type:
                    event.type = EventType.objects.get(id=type)
                    
                if admission:
                    event.admission = admission
                    
                if about:
                    event.about = about
                    
                if website:
                    event.website = website
                event.save()
                
                #Event Contact(s)
                contact = Contact.objects.create(
                    event=event,
                    person=contact_person,
                    phone=phone
                )
                if email:
                    contact.email = email
                if whatsapp:
                    contact.whatsapp = True
                contact.save()

                #gallery items
                poster = Poster.objects.create(
                    event=event,
                    image=main_poster,
                    main=True
                )
                
                if request.FILES['other_images']:
                    files = request.FILES.getlist('other_images')
                    for f in files:
                        Poster.objects.create(
                            event=event,
                            image=f
                        )
            else:
                template = "main/events/add.html"
                context = {
                    'EventForm': form,
                }
                return HttpResponse(render(request, template, context))
        else:
            pass