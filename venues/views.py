
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

from .forms import Venue as VenueForm
from .forms import EditVenue as EditForm

from .models import *
from utils.models import *
from events.models import *
from authentication.models import *

class Add(LoginRequiredMixin, View):
    login_url='/auth'

    def get(self, request):
        template = 'main/venues/add.html'
        context = {
            'form': VenueForm(),
        }
        return HttpResponse(render(request, template, context))

    def post(self, request):
        if 'add_venue' in request.POST:
            form = VenueForm(request.POST, request.FILES)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                suitable = form.cleaned_data.get('suitable')
                description = form.cleaned_data.get('description')
            
                #contacts
                website = form.cleaned_data.get('website')
                contact_person = form.cleaned_data.get('contact_person')
                phone = form.cleaned_data.get('phone')
                email = form.cleaned_data.get('email')
                
                #location
                street_address = form.cleaned_data.get('street_address')
                city = form.cleaned_data.get('city')
                latitude = form.cleaned_data.get('latitude')
                longitude = form.cleaned_data.get('longitude')

                v = Venue.objects.create(
                    name=name,
                    description=description,
                    website=website,
                    contact_person=contact_person,
                    phone=phone,
                    email=email,
                    street_address=street_address,
                    city=City.objects.get(id=city),
                    latitude=latitude,
                    longitude=longitude,
                    added_by=User.objects.get(id=request.user.id)
                )
                
                suitable_fors = form['suitable']
                sui_list = []
                if suitable_fors is not None:
                    for sui in suitable_fors.value():
                        s = EventPurpose.objects.get(id=sui)
                        sui_list.append(s)
                    v.suitable.set(sui_list)
                v.save()

                main_image = request.FILES['main_img']
                Images.objects.create(
                    venue=v,
                    image=main_image,
                    is_main=True
                )

                if request.FILES.get('other_img'):
                    files = request.FILES.getlist('other_img')
                    for f in files:
                        Images.objects.create(
                            venue=v,
                            image=f,
                            is_main=False
                        )
                messages.success(request, "Venue Added Successfully")
                return redirect(reverse('venues:post-venue'))
            else:
                template = 'main/venues/add.html'
                context = {
                    'form': form,
                }
                return HttpResponse(render(request, template, context))
            

class ViewVenue(View):
    def get(self, request, venue_id, slug=""):
        venue = get_object_or_404(Venue, id=venue_id)
        template = 'main/venues/view.html'
        context = {
            'featured':Event.objects.all().order_by('?')[:3],
            'similar': Venue.objects.all().exclude(id=venue.id).order_by('?')[:4],
            'venue':venue,
        }
        return HttpResponse(render(request, template, context))

class Index(View):
    def get(self, request):
        template = 'main/venues/index.html'
        venue_list = None
        #?page=2&query=&date_from=&date_to=&event_type=Party&city=Kwekwe%20-%20Zimbabwe&location=OLikjuhg
        if request.GET.get('query') is not None and request.GET.get('event_type') is not None and request.GET.get('event_type') != 'Any type':
            venue_list = Venue.objects.filter(name__icontains=request.GET.get('query'), type=Sub.objects.get(name=request.GET.get('event_type')))
        elif request.GET.get('query') is None and request.GET.get('event_type') is not None:
            venue_list = Event.objects.filter(type=EventType.objects.get(name=request.GET.get('event_type')))
        elif request.GET.get('query') is not None and (request.GET.get('event_type') is None or request.GET.get('event_type') =='Any type'):
            venue_list = Event.objects.filter(name__icontains=request.GET.get('query'))
        else:
            venue_list = Venue.objects.all().order_by('?')

        paginator = Paginator(venue_list, 9)
        page=request.GET.get('page', 1)

        venues = paginator.get_page(page)
        # Get the index of the current page
        index = venues.number - 1  # edited to something easier without index
        # This value is maximum index of your pages, so the last page - 1
        max_index = len(paginator.page_range)
        # You want a range of 7, so lets calculate where to slice the list
        start_index = index - 3 if index >= 3 else 0
        end_index = index + 3 if index <= max_index - 3 else max_index
        # Get our new page range. In the latest versions of Django page_range returns 
        # an iterator. Thus pass it to list, to make our slice possible again.
        page_range = list(paginator.page_range)[start_index:end_index]
        context = {
            'page_range':page_range,
            'types':EventType.objects.all(),
            'cities':City.objects.all(),
            'venues':venues
        }
        return HttpResponse(render(request, template, context))


class EditVenue(LoginRequiredMixin, View):
    login_url = '/auth'
    def get(self, request, venue_id, slug=''):
        venue = get_object_or_404(Venue, id=venue_id)
        if venue.added_by != User.objects.get(id=request.user.id):
            return HttpResponseForbidden()
        else:
            template = 'main/venues/edit.html'
            initial = {
                'name': venue.name,
                'suitable': [suitable.pk for suitable in venue.suitable.all()],
                'description':venue.description,
                'website':venue.website,
                'contact_person':venue.contact_person,
                'phone':venue.phone,
                'email':venue.email,
                'street_address':venue.street_address,
                'city':[venue.city.id, venue.city],
                'latitude':venue.latitude,
                'longitude':venue.longitude,
            }
            context = {
                'venue':venue,
                'form': EditForm(initial=initial),
            }
            return HttpResponse(render(request, template, context))

    def post(self, request, venue_id, slug=''):
        venue = get_object_or_404(Venue, id=venue_id)
        if venue.added_by != User.objects.get(id=request.user.id):
            return HttpResponseForbidden()
        else:
            form = EditForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                suitable = form.cleaned_data.get('suitable')
                description = form.cleaned_data.get('description')
            
                #contacts
                website = form.cleaned_data.get('website')
                contact_person = form.cleaned_data.get('contact_person')
                phone = form.cleaned_data.get('phone')
                email = form.cleaned_data.get('email')
                
                #location
                street_address = form.cleaned_data.get('street_address')
                city = form.cleaned_data.get('city')
                latitude = form.cleaned_data.get('latitude')
                longitude = form.cleaned_data.get('longitude')

                dict_updates = {
                    'name':name,
                    'description':description,
                    'website':website,
                    'contact_person':contact_person,
                    'phone':phone,
                    'email':email,
                    'street_address':street_address,
                    'city':City.objects.get(id=city),
                    'latitude':latitude,
                    'longitude':longitude,
                    'added_by':User.objects.get(id=request.user.id)
                }
                for key in dict_updates:
                    venue.key = dict_updates[key]
                
                # v = Venue.objects.filter(id=venue.id).update(**dict_updates).save()

                sui = form['suitable']
                sui_list = []
                if sui is not None:
                    for purpose in sui.value():
                        p = EventPurpose.objects.get(pk=str(purpose))
                        sui_list.append(p)
                    venue.suitable.set(sui_list)

                venue.save()

                messages.success(request, "Venue updated Successfully")
                template = 'main/venues/edit.html'
                context = {
                    'venue':venue,
                    'form': form,
                }
                return HttpResponse(render(request, template, context))
            else:
                template = 'main/venues/edit.html'
                context = {
                    'venue':venue,
                    'form': form,
                }
                return HttpResponse(render(request, template, context))

class My(LoginRequiredMixin, View):
    login_url = '/auth'
    def get(self, request):
        template = 'main/venues/my.html'
        context = {
            'venues':Venue.objects.filter(added_by=User.objects.get(id=request.user.id)).order_by('created_at')
        }
        return HttpResponse(render(request, template, context))

class Delete(LoginRequiredMixin, View):
    login_url = '/auth'
    def get(self, request, venue_id, slug=''):
        venue = get_object_or_404(Venue, id=venue_id)
        if venue.added_by != User.objects.get(id=request.user.id):
            return HttpResponseForbidden()
        else:
            if venue.delete():
                return redirect(reverse('venues:my'))