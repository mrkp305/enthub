'''
    Django Imports
'''

from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, Http404, HttpResponseForbidden, JsonResponse
from django.views import View
from django.views.defaults import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.files.base import ContentFile
from django.contrib import messages
from datetime import *
import json

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
                
                if request.FILES.get('other_images'):
                    files = request.FILES.getlist('other_images')
                    for f in files:
                        Poster.objects.create(
                            event=event,
                            image=f
                        )
                
                messages.success(request, 'Event Added Successfully. Manage your event(s) here.')
                return redirect(reverse('events:my-events'))
            else:
                template = "main/events/add.html"
                context = {
                    'EventForm': form,
                }
                return HttpResponse(render(request, template, context))
        else:
            pass

class My(LoginRequiredMixin, View):
    login_url = '/auth'
    def get(self, request):
        template = 'main/events/my.html'
        context = {
            'events':Event.objects.filter(added_by=User.objects.get(id=request.user.id)).order_by('created_at')
        }
        return HttpResponse(render(request, template, context))
    def post(self, request):
        pass

class Delete(LoginRequiredMixin, View):
    login_url = '/auth'
    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        if event.added_by != User.objects.get(id=request.user.id):
            return HttpResponseForbidden()
        else:
            if event.delete():
                messages.success(request, 'Event deleted successfully.')
                return redirect(reverse('events:my-events'))

class Details(LoginRequiredMixin, View):
    login_url = '/auth'
    def post(self, request):
        try:
            #2018-09-20 00:00:00+00:00
            event = Event.objects.get(id=request.POST.get('event'))
            data = {
                'Event name': event.name,
                'Type': event.type.name,
                'About': event.about,
                'Starts': event.end_date,
                'Ends': datetime.strftime(event.end_date, '%B %d, %Y @%I:%M hrs'),
                'Added By': event.added_by.first_name + ' ' + event.added_by.last_name,
                'Website': event.website,
                'Location': event.location.name,
                'Accepted?': 'Yes' if event.verified else 'Pending'
            }
            return JsonResponse(data)
        except Event.DoesNotExist as e:
            pass
            #2018-09-20T00:00:00Z

class Edit(LoginRequiredMixin, View):
    login_url = '/auth'
    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        if event.added_by != User.objects.get(id=request.user.id):
            return HttpResponseForbidden()
        else:
            initial = {
                'title':event.name,
                'type':[event.type.id, event.type],
                'about':event.about,
                'admission':event.admission,
                'start_date':event.start_date.strftime('%Y-%m-%d'),
                'start_time':event.start_date.time(),
                'end_date':event.end_date.strftime('%Y-%m-%d'),
                'end_time':event.end_date.time(),
                'website':event.website,
              
                'location_name':event.location.name,
                'street_address':event.location.street_address,
                'zip_code':event.location.zip_code,
                'city':[event.location.city.id, event.location.city],
                'latitude':event.location.latitude,
                'longitude':event.location.longitude,
            }
            template = 'main/events/edit.html'
            context = {
                'event':event,
                'EventForm': EditEvent(initial=initial)
            }
            return HttpResponse(render(request, template, context))

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        if event.added_by != User.objects.get(id=request.user.id):
            return HttpResponseForbidden()
        else:
            if 'update_event' in request.POST:
                form = EditEvent(request.POST)
                if form.is_valid():
                    title = form.cleaned_data.get('title')
                    type = form.cleaned_data.get('type')
                    start_date = form.cleaned_data.get('start_date')
                    start_time = form.cleaned_data.get('start_time')
                    end_date = form.cleaned_data.get('end_date')
                    end_time = form.cleaned_data.get('end_time')
                    admission = form.cleaned_data.get('admission')
                    
                    
                    location_name = form.cleaned_data.get('location_name')
                    city = form.cleaned_data.get('city')
                    street_address = form.cleaned_data.get('street_address')
                    zip_code = form.cleaned_data.get('zip_code')
                    latitude = form.cleaned_data.get('latitude')
                    longitude = form.cleaned_data.get('longitude')

                    about = form.cleaned_data.get('about')

                
                    website = form.cleaned_data.get('website')
                  
                    
                    #The Location first, since Event Object depends on it
                    location = Location.objects.get(
                        id=event.location.id
                    )
                    if location_name:
                        location.name = location_name

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
                    
                    
                    if title:
                        event.name = title
                        
                    if type:
                        event.type = EventType.objects.get(id=type)
                        
                    if admission:
                        event.admission = admission
                        
                    if about:
                        event.about = about
                        
                    if website:
                        event.website = website
                    event.save()
                    messages.success(request, 'Event Edited successfully')
                    return redirect(reverse('events:my-events'))
                else:
                    template = 'main/events/edit.html'
                    context = {
                        'event':event,
                        'EventForm': form
                    }
                    messages.error(request, 'Something wrong with your input. Please check Again')
                    return HttpResponse(render(request, template, context))
            else:
                return HttpResponseForbidden()



class EditLocation(LoginRequiredMixin, View):
    login_url = '/auth'
    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        if event.added_by != User.objects.get(id=request.user.id):
            return HttpResponseForbidden()
        else:
            template = 'main/events/edit-location.html'
            context = {
                'event':event,
                'form':EditLocationForm(initial=initial)
            }
            return HttpResponse(render(request, template, context))
    
    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        if event.added_by != User.objects.get(id=request.user.id):
            return HttpResponseForbidden()
        else:
            if 'edit_location' in request.POST:
                form = EditLocationForm(request.POST)
                if form.is_valid():
                    pass
                else:
                    template = 'main/events/edit-location.html'
                    context = {
                        'event':event,
                        'form':form
                    }
                    messages.error(request, 'Please check your input and try again.')
                    return HttpResponse(render(request, template, context))




