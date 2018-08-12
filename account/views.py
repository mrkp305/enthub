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
        initial = {
            'name':request.user,
            'handle':request.user.profile.handle,
            'email':request.user.email,
            'phone':request.user.profile.phone,
            'bio':request.user.profile.bio,
            'tags':[tag.pk for tag in request.user.profile.tags.all()],
            'city':[request.user.profile.city.id, request.user.profile.city.name] if request.user.profile.city is not None else None
        }
        context = {
            'ProfileForm':ProfileForm(initial=initial),
        }
        return HttpResponse(render(request, template, context))
    