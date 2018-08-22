from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.defaults import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import re
from .forms import *
from events.models import Event
from artists.models import Artist
from venues.models import Venue
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site

class Home(View):
    def get(self, request):
        template = 'main/home.html'
        meta = {
            'description':'EntHub is your goto Zimbabwean events broadcaster and entertainment promoter. Here you also find artists and venues in the directory.',
            'og':{
                'title':'EntHub. Zimbabwe\' biggest entertainment hub',
                'url':str(get_current_site(request))+request.path,
                'type':'website',
                'description':'EntHub is your goto Zimbabwean events broadcaster and entertainment promoter. Here you also find artists and venues in the directory.',
                'image': ''
            },
            'twitter':{
                'card':'EntHub.Your entertainment Companion',
                'title':'EntHub. Zimbabwe\' biggest entertainment hub and artist directory',
                'description':'EntHub is your goto Zimbabwean events broadcaster and entertainment promoter. Here you also find artists and venues in the directory.',
                'url':str(get_current_site(request))+request.path,
                'image':''
            }
        }
        context = {
            'artists': Artist.objects.order_by('?')[:15],
            'this_week':Event.objects.order_by('?')[:10],
            'events': Event.objects.all()[:25],
            'venues': Venue.objects.all()[:25],
            'meta':meta,
        }
        return HttpResponse(render(request, template, context))
class Tos(View):
    
    def get(self, request):
        template = 'main/tos.html'
        meta = {
            'description':'Please read our terms of service before using any our services.',
            'og':{
                'title':'EntHub Terms of Service ',
                'url':str(get_current_site(request))+request.path,
                'type':'website',
                'description':'Please read our terms of service before using any our services.',
                'image': ''
            },
            'twitter':{
                'card':'EntHub Terms of Service',
                'title':'EntHub Terms of service',
                'description':'Please read our terms of service before using any our services.',
                'url':str(get_current_site(request))+request.path,
                'image':''
            }
        }
        context = {
            'meta':meta,
        }
        return HttpResponse(render(request, template, context))

class CoPolicy(View):
    
    def get(self, request):
        template = 'main/cop.html'
        meta = {
            'description':'Please read our copyright policy before using any our services.',
            'og':{
                'title':'EntHub Copyright policy ',
                'url':str(get_current_site(request))+request.path,
                'type':'website',
                'description':'Please read our copyright policy before using any our services.',
                'image': ''
            },
            'twitter':{
                'card':'EntHub Copyright Policy',
                'title':'EntHub Copyright policy ',
                'url':str(get_current_site(request))+request.path,
                'type':'website',
                'description':'Please read our copyright policy before using any our services.',
                'image': ''
            }
        }
        context = {
            'meta':meta,
        }
        return HttpResponse(render(request, template, context))

class PrPolicy(View):
    
    def get(self, request):
        template = 'main/prp.html'
        meta = {
            'description':'Please read our privacy policy before using any our services.',
            'og':{
                'title':'EntHub Privacy policy ',
                'url':str(get_current_site(request))+request.path,
                'type':'website',
                'description':'Please read our privacy policy before using any our services.',
                'image': ''
            },
            'twitter':{
                'card':'EntHub privacy Policy',
                'title':'EntHub privacy policy ',
                'url':str(get_current_site(request))+request.path,
                'type':'website',
                'description':'Please read our privacy policy before using any our services.',
                'image': ''
            }
        }
        context = {
            'meta':meta,

        }
        return HttpResponse(render(request, template, context))

