from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.defaults import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
import re
from .forms import *
from .models import *
from account.models import *

# Create your views here.
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
            if form.is_valid():
                user = authenticate(email=form.cleaned_data['email_address'], password=form.cleaned_data['password'])
                if user is not None:
                    login(request, user)
                    return redirect('/account/profile')
                else:
                    context = {
                        'LoginForm': form,
                        'RegisterForm': SignUp(),
                        'ActiveTab': 'tabLogin',
                        'InActiveTab': 'tabRegister',
                        'ActiveLink': 'loginToggle',
                        'InActiveLink': 'registerToggle',
                        'ShiftFocus': 1,
                    }
                    messages.add_message(request, messages.ERROR, 'Login Failed! Invalid account credentials.')
                    return HttpResponse(render(request, self.template, context))
            else:
                context = {
                    'LoginForm':form,
                    'RegisterForm': SignUp(),
                    'ActiveTab': 'tabLogin',
                    'InActiveTab': 'tabRegister',
                    'ActiveLink': 'loginToggle',
                    'InActiveLink': 'registerToggle',
                    'ShiftFocus': 1,
                }
                messages.add_message(request, messages.WARNING, 'Invalid input.')
                return HttpResponse(render(request, self.template, context))
        else:
            form = SignUp(request.POST)
            if form.is_valid():
                account = User.objects.create_user(form.cleaned_data['email_address'], form.cleaned_data['password'])
                firstname, lastname = form.cleaned_data['name'].split()
                account.first_name = firstname
                account.last_name = lastname
                account.save()

                profile = Profile.objects.create(user=account)
                profile.save()
                # profile = account.
                user = authenticate(email=form.cleaned_data['email_address'], password=form.cleaned_data['password'])
                login(request, user)
                return redirect('/account/profile')
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


