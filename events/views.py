'''
    Django Imports
'''

from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, Http404
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

from .forms import *


'''
    End form imports
'''

'''Model Imports
'''
from .models import *
from utils.models import *

class Events(View):
    def get(self, request):
        pass