from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.defaults import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate, login
from account.models import Profile as UserProfile
from .forms import Profile as ProfileForm
from .forms import Avatar as AvatarForm
import base64
from django.core.files.base import ContentFile
import os

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

    def post(self, request):
        if 'update_avatar' in request.POST:
            form = AvatarForm(request.POST)
            if form.is_valid():
                '''
                    Delete Old Image\If any.

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
        else:
            pass
    