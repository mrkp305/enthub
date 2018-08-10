from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.defaults import *
import re

class Home(View):
    def get(self, request):
        template = 'main/home.html'
        context = {

        }
        return HttpResponse(render(request, template, context))
