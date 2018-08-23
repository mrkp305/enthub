'''Django Imports
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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

''' End Django Imports
'''


''' Form Imports
'''

from .forms import *


''' End form imports
'''

'''Model Imports
'''
from .models import *
from utils.models import *
from authentication.models import User
from django.contrib.sites.shortcuts import get_current_site

class Map(View):
    def get(self, request):
        t = 'main/events/map.html'
        meta = {
            'description':'Browse and Explore events near you using a map.',
            'og':{
                'title':'Map Browser',
                'url':str(get_current_site(request))+request.path,
                'type':'website',
                'description':'Browse and Explore events near you using a map.',
                'image': ''
            },
            'twitter':{
                'card':'EntHub event map browser.',
                'title':'Map Browser',
                'url':str(get_current_site(request))+request.path,
                'type':'website',
                'description':'Browse and Explore events near you using a map.',
                'image': ''
            }
        }
        context = {
            'meta':meta,

        }
        return HttpResponse(render(request, t, context))
    
class Add(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/auth'
    def test_func(self):
        return True

    def get(self, request):
        template = "main/events/add.html"
        meta = {
            'description':'Post an event to a larger audience on EntHub.',
            'og':{
                'title':'Post Event',
                'url':str(get_current_site(request))+request.path,
                'type':'website',
                'description':'Post your events here to reach a guaranteed larger audience.',
                'image': ''
            },
            'twitter':{
                'card':'Post your event on EntHub',
                'title':'Post Event',
                'url':str(get_current_site(request))+request.path,
                'type':'website',
                'description':'Post your events here to reach a guaranteed larger audience.',
                'image': ''
            }
        }
        context = {
            'meta':meta,
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
                meta = {
                    'description':'Post an event to a larger audience on EntHub.',
                    'og':{
                        'title':'Post Event',
                        'url':str(get_current_site(request))+request.path,
                        'type':'website',
                        'description':'Post your events here to reach a guaranteed larger audience.',
                        'image': ''
                    },
                    'twitter':{
                        'card':'Post your event on EntHub',
                        'title':'Post Event',
                        'url':str(get_current_site(request))+request.path,
                        'type':'website',
                        'description':'Post your events here to reach a guaranteed larger audience.',
                        'image': ''
                    }
                }
                context = {
                    'meta':meta,
                    'EventForm': form,
                }
                return HttpResponse(render(request, template, context))
        else:
            pass

class My(LoginRequiredMixin, View):
    login_url = '/auth'
    def get(self, request):
        template = 'main/events/my.html'
        meta = {
            'description':'These are the events you\'ve posted. Here you can manage them.',
            'og':{
                'title':'Your Events',
                'url':str(get_current_site(request))+request.path,
                'type':'website',
                'description':'These are the events you\'ve posted. Here you can manage them.',
                'image': ''
            },
            'twitter':{
                'card':'Manage your events.',
                'title':'Your Events',
                'url':str(get_current_site(request))+request.path,
                'type':'website',
                'description':'These are the events you\'ve posted. Here you can manage them.',
                'image': ''
            }
        }
        context = {
            'meta':meta,
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
            event = Event.objects.get(id = request.POST.get('event'))
            
            data = {
                'Event name': event.name,
                'Type': event.type.name,
                'About': event.about,
                'Starts': datetime.strftime(event.start_date, '%B %d, %Y @%H:%M hrs'),
                'Ends': datetime.strftime(event.end_date, '%B %d, %Y @%H:%M hrs'),
                'Added By': event.added_by.first_name + ' ' + event.added_by.last_name,
                'Website': event.website,
                'Location': event.location.name,
                'Accepted?': 'Yes' if event.verified else 'Pending'
            }
            return JsonResponse(data)
        except Event.DoesNotExist as e:
            pass
            #2018-09-20T00:00:00Z

class GeoData(View):
    def get(self, request):
        
        events = {'events':[]}
        for event in Event.objects.all():
            html = "<div class='mapx-box' style=\"font-family:'Varela Round' !important;color:#fff !important;\">\
                    <img src='{}'>\
                    <h5 style='color:#fff !important'><a style='color:#fff !important' href='/events/{}/'>{}</a></h5>\
                    <p>{}</p></div>".format(event.get_poster_url(),event.id, event.name, datetime.strftime(event.start_date,'%b %d'))
            data = {
                'name':event.name,
                'lat':event.location.latitude,
                'lon':event.location.longitude,
                'html':html,
            }
            events['events'].append(data)
        return JsonResponse(events)
       

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
            meta = {
                'description':'Modifying an event you\'ve posted.',
                'og':{
                    'title':'Edit event',
                    'url':str(get_current_site(request))+request.path,
                    'type':'website',
                    'description':'Modifying an event you\'ve posted.',
                    'image': ''
                },
                'twitter':{
                    'card':'Manage your events.',
                    'title':'Edit event',
                    'url':str(get_current_site(request))+request.path,
                    'type':'website',
                    'description':'Modifying an event you\'ve posted.',
                    'image': ''
                }
            }
            context = {
                'meta':meta,
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
                        event=event
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

                    event.start_date=datetime.combine(start_date, start_time)
                    event.end_date=datetime.combine(end_date, end_time)
                    
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


class Events(View):
    def get(self, request):
        event_list = None
        #?page=2&query=&date_from=&date_to=&event_type=Party&city=Kwekwe%20-%20Zimbabwe&location=OLikjuhg
        if request.GET.get('query') is not None and request.GET.get('event_type') is not None and request.GET.get('event_type') != 'Any type':
            event_list = Event.objects.filter(name__icontains=request.GET.get('query'), type=EventType.objects.get(name=request.GET.get('event_type')))
        elif request.GET.get('query') is None and request.GET.get('event_type') is not None:
            event_list = Event.objects.filter(type=EventType.objects.get(name=request.GET.get('event_type')))
        elif request.GET.get('query') is not None and (request.GET.get('event_type') is None or request.GET.get('event_type') =='Any type'):
            event_list = Event.objects.filter(name__icontains=request.GET.get('query'))
        else:
            event_list = Event.objects.all().order_by('start_date')

        paginator = Paginator(event_list, 9)
        page=request.GET.get('page', 1)

        template = 'main/events/index.html'
        events = paginator.get_page(page)
        # Get the index of the current page
        index = events.number - 1  # edited to something easier without index
        # This value is maximum index of your pages, so the last page - 1
        max_index = len(paginator.page_range)
        # You want a range of 7, so lets calculate where to slice the list
        start_index = index - 3 if index >= 3 else 0
        end_index = index + 3 if index <= max_index - 3 else max_index
        # Get our new page range. In the latest versions of Django page_range returns 
        # an iterator. Thus pass it to list, to make our slice possible again.
        page_range = list(paginator.page_range)[start_index:end_index]
        meta = {
            'description':'Browse and Explore events from around Zimbabwe',
            'og':{
                'title':'EntHub Events Listings',
                'url':str(get_current_site(request))+request.path,
                'type':'website',
                'description':'Browse and Explore events from around Zimbabwe',
                'image': ''
            },
            'twitter':{
                'card':'Explore events from around Zimbabwe.',
                'title':'EntHub Events Listings',
                'url':str(get_current_site(request))+request.path,
                'type':'website',
                'description':'Browse and Explore events from around Zimbabwe',
                'image': ''
            }
        }
        context = {
            'meta':meta,
            'page_range':page_range,
            'types':EventType.objects.all(),
            'cities':City.objects.all(),
            'locations':Location.objects.all(),
            'events':events
        }
        return HttpResponse(render(request, template, context))

class ViewEvent(View):
    def get(self, request, id, slug=""):
        event_id=id
        event = get_object_or_404(Event, id=event_id)
        featured = Event.objects.exclude(id=event.id)[:3]
        similar = Event.objects.filter(type=event.type).exclude(id=event.id)[:5]
        template = 'main/events/view.html'
        meta = {
            'description':event.about,
            'keywords':str(event.name) + ', '+str(event.type) +', event, zimbabwe entertainment, ' + str(event.location.city.name) +','+str(event.added_by),
            'og':{
                'title':event.name,
                'url':str(get_current_site(request))+request.path,
                'type':'website',
                'description':event.about,
                'image': event.get_poster_url
            },
            'twitter':{
                'card':'Explore events from around Zimbabwe.',
                'title':event.name,
                'url':str(get_current_site(request))+request.path,
                'type':'website',
                'description':event.about,
                'image': event.get_poster_url
            }
        }
        context = {
            'meta':meta,
            'event':event,
            'featured':featured,
            'similar':similar,
            
        }
        return HttpResponse(render(request, template, context))
    
class Calendar(View):
    def get(self, request):
        template = "main/events/calendar.html"
        meta = {
            'description':'Track your favourite events on EntHub on our EventsCalendar app here.',
            'og':{
                'title':'Events Calendar',
                'url':str(get_current_site(request))+request.path,
                'type':'website',
                'description':'Track your favourite events on EntHub on our EventsCalendar app here.',
                'image': ''
            },
            'twitter':{
                'card':'Track events on the calendar here on EntHub',
                'title':'Events Calendar',
                'url':str(get_current_site(request))+request.path,
                'type':'website',
                'description':'Track your favourite events on EntHub on our EventsCalendar app here.',
                'image': ''
            }
        }
        context = {
            'meta':meta,

        }
        return HttpResponse(render(request, template, context))


class CalendarJson(View):
    def get(self, request):
        '''
            $start = date('Y-m-d', strtotime($_POST['start']));
            $end = date('Y-m-d', strtotime($_POST['end']));
        '''
        start_date = datetime.strptime(request.GET.get('start'), '%Y-%m-%d')
        end_date = datetime.strptime(request.GET.get('end'), '%Y-%m-%d')
        events = Event.objects.filter(start_date__range=(start_date, end_date))
        blob = {'result':[]}
        for event in events:
            dta = {
                'id': event.id,
                'title': event.name,
                'start': event.start_date,
                'end': event.end_date,
                'poster': event.get_poster_url(),
                'about': event.about,
                'venue': event.location.name,
                'address' :event.location.street_address,
                'city': event.location.city.name,
                'date': event.start_date,
                'time': '4S',
                'link':'jnbn'
            }
            blob['result'].append(dta)
        return JsonResponse(blob)
