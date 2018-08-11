from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.defaults import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import re
from .forms import *

class Home(View):
    def get(self, request):
        template = 'main/home.html'
        context = {

        }
        return HttpResponse(render(request, template, context))

class Auth(View):
    template = 'main/auth.html'
    def get(self, request):
        context = {
            'LoginForm': SignIn(),
            'RegisterForm': SignUp(),
            'InActiveTab': 'tabRegister',
            'ActiveTab': 'tabLogin',
            'ActiveLink': 'loginToggle',
            'InActiveLink': 'registerToggle',
            'ShiftFocus': 0,
        }
        return HttpResponse(render(request, self.template, context))

    def post(self, request):
        if 'login' in request.POST:
            form = SignIn(request.POST)
        else:
            form = SignUp(request.POST)
            if form.is_valid():
                return HttpResponse("Yaaay")
            else:
                context = {
                    'LoginForm': SignIn(),
                    'RegisterForm': form,
                    'ActiveTab': 'tabRegister',
                    'InActiveTab': 'tabLogin',
                    'ActiveLink': 'registerToggle',
                    'InActiveLink': 'loginToggle',
                    'ShiftFocus': 1,
                }
                return HttpResponse(render(request, self.template, context))


class Profile(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/auth/'
    def get(self, request):
        template = 'main/account/profile.html'
        context = {

        }
        return HttpResponse(render(request, template, context))
