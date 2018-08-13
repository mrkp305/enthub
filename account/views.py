'''
    Django Imports
'''

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.defaults import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate, login
from django.core.files.base import ContentFile
from django.contrib import messages

'''
    End Django Imports
'''


'''
    Models
'''
from authentication.models import User
from account.models import Profile as UserProfile
from account.models import Social as SocialProfile
from utils.models import City, Tag
'''
    End Models
'''


'''
    Forms

'''

from .forms import Profile as ProfileForm
from .forms import Avatar as AvatarForm

'''
    End Forms
'''


'''
    Python Imports
'''

import base64
import os

'''
    End Python Imports
'''


class Profile(LoginRequiredMixin, View):
    login_url = '/auth/'
    def get(self, request):
        template = 'main/account/profile.html'
        ProfileInitial = {
            'name':request.user,
            'handle':request.user.profile.handle,
            'email':request.user.email,
            'phone':request.user.profile.phone,
            'bio':request.user.profile.bio,
            'tags':[tag.pk for tag in request.user.profile.tags.all()],
            'city':[request.user.profile.city.id, request.user.profile.city.name] if request.user.profile.city is not None else None,
            'twitter':request.user.profile.social.twitter if request.user.profile.social is not None else None,
            'facebook':request.user.profile.social.facebook if request.user.profile.social is not None else None,
            'instagram':request.user.profile.social.instagram if request.user.profile.social is not None else None,
            'google':request.user.profile.social.google if request.user.profile.social is not None else None,
        }
        context = {
            'ProfileForm':ProfileForm(initial=ProfileInitial),
        }
        return HttpResponse(render(request, template, context))

    def post(self, request):
        if 'update_avatar' in request.POST:
            form = AvatarForm(request.POST)
            if form.is_valid():
                '''
                    Delete Old Image **if any.

                '''
                if request.user.profile.avatar is not None:
                    try:
                        os.remove(request.user.profile.avatar.path)
                    except Exception as e:
                        pass

                data = form.cleaned_data['base64image']
                format, imgstr = data.split(';base64,') 
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name='image.' + ext)
                profile = UserProfile.objects.get(user=request.user)
                profile.avatar = data
                profile.save()
                return redirect('/account/profile')
            else:
                return HttpResponse(form.errors['update_avatar'])
        elif 'update_profile_defails' in request.POST:
            form = ProfileForm(request.POST)
            if form.is_valid():
                template = 'main/account/profile.html'

                user = User.objects.get(pk=request.user.id)
                profile = UserProfile.objects.get(user=user)
                social_profile = SocialProfile.objects.get(profile=profile)

                name = form.cleaned_data['name']
                if "{} {}".format(request.user.first_name, request.user.last_name) != name:
                    user.first_name = name.split()[0]
                    user.last_name = name.split()[1]

                handle = form.cleaned_data['handle']
                if request.user.profile.handle != handle:
                    profile.handle = handle

                email = form.cleaned_data['email']
                if request.user.email != email:
                    user.email = email

                phone = form.cleaned_data['phone']
                if request.user.profile.phone != phone:
                    profile.phone = phone

                bio = form.cleaned_data['bio']
                if request.user.profile.bio != bio:
                    profile.bio = bio

                tags = form['tags']
                tag_list = []
                if tags is not None:
                    for tag in tags.value():
                        t = Tag.objects.get(pk=str(tag))
                        tag_list.append(t)
                    profile.tags.set(tag_list)


                city = form.cleaned_data['city']
                if request.user.profile.city != city:
                    profile.city = City.objects.get(id=city)

                twitter = form.cleaned_data['twitter']
                if request.user.profile.social.twitter != twitter:
                    social_profile.twitter = twitter

                facebook = form.cleaned_data['facebook']
                if request.user.profile.social.facebook != facebook:
                    social_profile.facebook = facebook

                instagram = form.cleaned_data['instagram']
                if request.user.profile.social.instagram != instagram:
                    social_profile.instagram = instagram

                google = form.cleaned_data['google']
                if request.user.profile.social.google != google:
                    social_profile.google = google

                user.save()
                profile.save()
                social_profile.save()

                messages.add_message(request, messages.SUCCESS, 'Profile Info Updated Successfully')
                
                return redirect('/account/profile')
            else:
                template = 'main/account/profile.html'
                messages.error(request, 'There was something wrong with your input. Please check again.')
                context = {
                    'ProfileForm':form,
                }
                return HttpResponse(render(request, template, context))
        else:
            pass
    