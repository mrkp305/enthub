'''
    Django Imports
'''

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.defaults import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.files.base import ContentFile
from django.contrib import messages

'''
    End Django Imports
'''


'''
    Form Imports
'''

from .forms import Profile as ArtistProfileForm
from .forms import Contact as ArtistContactsForm

'''
    End form imports
'''

'''Model Imports
'''
from .models import Artist as Profile
from .models import Contact
from utils.models import *

class CreateProfile(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/auth'
    def test_func(self):
        return not self.request.user.profile.artist

    def get(self, request):
        template = 'main/artists/create-profile.html'
        context = {
            'form':ArtistProfileForm(),
        }
        return HttpResponse(render(request, template,context))
    
    def post(self, request):
        if 'create_artist_profile' in request.POST:
            form = ArtistProfileForm(request.POST)
            if form.is_valid():
                stage_name = form.cleaned_data['stage_name']
                alias = form.cleaned_data['alias']
                genre = form.cleaned_data['genre']
                bio = form.cleaned_data['bio']
                dob = form.cleaned_data['dob']

                artist_profile = Profile.objects.create(
                    user_profile=request.user.profile,
                    stage_name=stage_name,
                    alias=alias,
                    genre = Genre.objects.get(pk=genre),
                    bio = bio,
                    dob = dob
                    )
                artist_profile.save()
                messages.success(request, 'Artist Profile Created Successfully. Click <a href="#">here</a> to edit profile.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                messages.error(request, 'There was something with the information you just supplied. Try again.')
                template = 'main/artists/create-profile.html'
                context = {
                    'form':form,
                }
                return HttpResponse(render(request, template,context))
        else:
            pass


class MyProfile(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/auth'
    def test_func(self):
        return self.request.user.profile.artist

    def get(self, request):
        template = 'main/artists/my-profile.html'
        context = {
            'ProfileForm':ArtistProfileForm()
        }
        return HttpResponse(render(request, template,context))

class Contacts(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/auth'
    def test_func(self):
        return self.request.user.profile.artist

    def get(self, request):
        template = 'main/artists/my-contacts.html'
        context = {
            'ContactForm':ArtistContactsForm()
        }
        return HttpResponse(render(request, template,context))

    def post(self, request):
        if 'person' and 'purpose' and 'phone' and 'email' in request.POST:
            form = ArtistContactsForm(request.POST)
            if form.is_valid():
                messages.success(request, 'Contact saved successfully.')
                con = Contact.objects.create(
                    artist=request.user.profile.artist,
                    person=form.cleaned_data.get('person'),
                    purpose=form.cleaned_data.get('purpose'),
                    phone=form.cleaned_data.get('phone'),
                    email=form.cleaned_data.get('email'),
                    )
                con.save()
                template = 'main/artists/my-contacts.html'
                context = {
                    
                    'ContactForm':ArtistContactsForm(),
                }
                return HttpResponse(render(request, template,context))
            else:
                messages.error(request, 'Invalid input. Check and try again.')
                template = 'main/artists/my-contacts.html'
                context = {
                    'ContactForm':form,
                }
                return HttpResponse(render(request, template,context))