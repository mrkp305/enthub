'''
    Django Imports
'''
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, Http404
from django.views import View
from django.views.defaults import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

'''
    End Django Imports
'''


'''
    Python Imports
'''
import re
'''
    End Python Imports
'''


'''
    Form Imports
'''
from .forms import *
'''
    End Form Imports
'''


'''
    Model Imports
'''
from .models import *
from account.models import *

'''
    End Model Imports
'''


class Auth(View):
    template = 'main/auth.html'
    def get(self, request):
        shift_focus = 0
        if request.session['changed_password'] is not None:
            if request.session.get('changed_password') == True:
                shift_focus = 1

        context = {
            'LoginForm': SignIn(),
            'RegisterForm': SignUp(),
            'InActiveTab': 'tabRegister',
            'ActiveTab': 'tabLogin',
            'ActiveLink': 'loginToggle',
            'InActiveLink': 'registerToggle',
            'ShiftFocus': shift_focus,
        }
        return HttpResponse(render(request, self.template, context))

    def post(self, request):
        if request.session.get('changed_password') is not None:
            del request.session['changed_password']

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
        elif 'register' in request.POST:
            form = SignUp(request.POST)
            if form.is_valid():
                account = User.objects.create_user(form.cleaned_data['email_address'], form.cleaned_data['password'])
                firstname, lastname = form.cleaned_data['name'].split()
                account.first_name = firstname
                account.last_name = lastname
                account.save()

                profile = Profile.objects.create(user=account)
                profile.save()

                social_profile = Social.objects.create(profile=profile)
                social_profile.save()
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

class Logout(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('/')

class ChangePassword(LoginRequiredMixin, View):
    login_url = '/auth'
    def get(self, request):
        template = 'main/change-password.html'
        context = {
            'form':ChangePasswordForm(),
        }
        return HttpResponse(render(request, template, context))
    
    def post(self, request):
        if 'change_password' in request.POST:
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                old = form.cleaned_data.get('old_password')
                new = form.cleaned_data.get('new_password')
                user = User.objects.get(email=request.user.email)
                if user.check_password(old):
                    user.set_password(new)
                    user.save()
                    messages.success(request, 'Password successfully changed')
                    request.session['changed_password'] = True
                    return redirect(reverse('authentication:change-password'))
                else:
                    messages.error(request, 'Task failed. Wrong password.')
                    form.add_error('old_password', 'Wrong password.')
                    template = 'main/change-password.html'
                    context = {
                        'form':form,
                    }
                    return HttpResponse(render(request, template, context))
            else:
                messages.error(request, 'Something wrong with your input. Please check and try again.')
                template = 'main/change-password.html'
                context = {
                    'form':form,
                }
                return HttpResponse(render(request, template, context))
        else:
            #to-do Change to 403
            raise (Http404)