'''Django Imports
'''
from django import forms
from django.core.validators import URLValidator
'''End Django Imports
'''

'''Model Imports
'''

from utils.models import City, Tag
from authentication.models import User

'''End Model Imports
'''


'''
    Python Imports
'''

import re
import base64
    
'''
    End Python Imports
'''


city_list = []
try:
    for c in City.objects.all():
        city_list.append([c.id,c])
except Exception as e:
    pass

tags = []
try:
    for t in Tag.objects.all():
        tags.append([t.id, t.name])
except Exception as e:
    pass

class Profile(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), max_length=30, required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'input-text'}), required=True)
    handle = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), max_length=30, required=False)
    city = forms.CharField(widget=forms.Select(choices=city_list, attrs={'class':'chosen-select-no-single'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), max_length=15, required=False)
    tags = forms.CharField(widget=forms.SelectMultiple(choices=tags, attrs={'name':'tags[]','class':'chosen-select-no-single','placeholder':'Select tags'}), required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'cols':'30','rows':'10'}), required=False)
    twitter = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), required=False)
    facebook = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), required=False)
    instagram = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), required=False)
    google = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), required=False)
    
    
    def clean(self):
        cleaned_data = super(Profile, self).clean()

        name = cleaned_data.get('name')
        handle = cleaned_data.get('handle')
        city = cleaned_data.get('city')
        phone = cleaned_data.get('phone')
        tags = cleaned_data.get('tags')
        twitter = cleaned_data.get('twitter')
        facebook = cleaned_data.get('facebook')
        instagram = cleaned_data.get('instagram')
        google = cleaned_data.get('google')

        if name:
            if not len(name.split()) > 1:
                self.add_error('name', 'Please enter full name.')
            elif len(name.split()) > 2:
                self.add_error('name', 'Please enter only first and last names.')
            else:
                regex = re.compile(r'^[a-zA-Z]{2,}[\s][a-zA-Z]{2,}$', re.U)
                if not regex.match(name):
                    self.add_error('name', 'Please enter a valid name.')

        if handle:
            if len(handle) < 5:
                self.add_error('handle', 'Your handle should be at least 5 characters.')
            elif len(handle) > 15:
                self.add_error('handle', 'Your handle should be at most 15 characters.')
            else:
                regex = re.compile(r'[a-zA-Z0-9]+$', re.U)
                if not regex.match(handle):
                    self.add_error('handle', 'Your handle should only contain letters and numbers.')

        if phone:
            regex = re.compile(r'^\+?1?\d{9,15}$')
            if not regex.match(phone):
                self.add_error('phone', 'Please enter a valid phone number.')

        if tags:
            pass

        if city:
            try:
                c = City.objects.get(pk=city)
            except Exception as e:
                self.add_error('city', 'City not found')

        if twitter:
            try:
                validate = URLValidator(schemes=('http', 'https'))
                validate(twitter)
            except Exception as e:
                self.add_error('twitter',"Invalid URL")
        
        if facebook:
            try:
                validate = URLValidator(schemes=('http', 'https'))
                validate(facebook)
            except Exception as e:
                self.add_error('facebook', 'Invalid URL')
        
        if instagram:
            try:
                validate = URLValidator(schemes=('http', 'https'))
                validate(instagram)
            except Exception as e:
                self.add_error('instagram', 'Invalid URL')
        
        if google:
            try:
                validate = URLValidator(schemes=('http', 'https'))
                validate(google)
            except Exception as e:
                self.add_error('google', 'Invalid URL')


class Avatar(forms.Form):
    update_avatar = forms.CharField(widget=forms.HiddenInput(), required=True)
    base64image = forms.CharField(widget=forms.HiddenInput(), required=True)

    def clean(self):
        cleaned_data = super(Avatar, self).clean()
        update_avatar = cleaned_data.get('update_avatar')
        
        if update_avatar != '1':
            self.add_error('update_avatar', 'Action Unauthorized')
        

