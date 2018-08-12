from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.defaults import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
# Create your views here.
from .forms import Profile as ProfileForm

class Profile(LoginRequiredMixin, View):
    login_url = '/auth/'
    def get(self, request):
        template = 'main/account/profile.html'
        context = {
            'ProfileForm':ProfileForm(),
        }
        return HttpResponse(render(request, template, context))
    