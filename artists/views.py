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

class CreateProfile(LoginRequiredMixin, View):
    login_url = '/auth'
    def get(self, request):
        pass