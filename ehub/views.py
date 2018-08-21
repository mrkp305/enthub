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

class Home(View):
    def get(self, request):
        template = 'main/home.html'
        context = {
            'artists': Artist.objects.order_by('?')[:15],
            'this_week':Event.objects.order_by('?')[:10],
            'events': Event.objects.all()[:25],
            'venues': Venue.objects.all()[:25],
        }
        return HttpResponse(render(request, template, context))
class Tos(View):
    
    def get(self, request):
        template = 'main/tos.html'
        context = {

        }
        return HttpResponse(render(request, template, context))

class CoPolicy(View):
    
    def get(self, request):
        template = 'main/cop.html'
        context = {

        }
        return HttpResponse(render(request, template, context))

class PrPolicy(View):
    
    def get(self, request):
        template = 'main/prp.html'
        context = {

        }
        return HttpResponse(render(request, template, context))

