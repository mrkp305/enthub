'''
    Django Imports
'''
from django import forms
from django.core.validators import URLValidator
'''
    End Django Imports
'''

'''
    Other Model Imports
'''
from utils.models import *
from django.utils.translation import ugettext_lazy as _
'''
    End Other Model Imports
'''


'''
    Python Imports
'''
import re
'''
    End python Imports
'''



genres = []
try:
    for genre in Genre.objects.all():
        genres.append([genre.pk,genre])
except Exception as e:
    pass
    
class DateInput(forms.DateInput):
    input_type = 'date'

class Profile(forms.Form):

    stage_name = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), max_length=30, required=True)
    genre = forms.CharField(widget=forms.Select(choices=genres, attrs={'class':'chosen-select-no-single'}))
    alias = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), max_length=30, required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'class':'input-text'}))
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'class':'input-text', 'type':'date'}))
    website = forms.URLField(widget=forms.TextInput(attrs={'class':'input-text'}), required=False)

    def clean(self):
        cleaned_data = super(Profile, self).clean()
        stage_name = cleaned_data.get('stage_name')
        genre = cleaned_data.get('genre')
        alias = cleaned_data.get('alias')
        dob = cleaned_data.get('dob')
        website = cleaned_data.get('website')

        if stage_name:
            if len(stage_name) < 2:
                self.add_error('stage_name', 'Stage name should be at least 2 characters.')
            elif len(stage_name) > 15:
                self.add_error('stage_name', 'Stage name should be at most 15 characters.')
            else:
                # r'^[a-zA-Z]{2,}[\s][a-zA-Z]{2,}$', re.U
                regex = re.compile(r'[a-zA-Z0-9\s]+$', re.U)
                if not regex.match(stage_name):
                    self.add_error('stage_name', 'Stage name should only contain letters or numbers.')
    
        if genre:
            try:
                genre = Genre.objects.get(pk=genre)
            except Exception as e:
                self.add_error('genre', 'Genre selected does not exist.')

        if alias:
            if len(alias) < 2:
                self.add_error('alias', 'Alias should be at least 2 characters.')
            elif len(alias) > 15:
                self.add_error('alias', 'Alias should be at most 15 characters.')
            else:
                regex = re.compile(r'[a-zA-Z0-9\s]+$', re.U)
                if not regex.match(alias):
                    self.add_error('alias', 'Alias should only contain letters and/or numbers.')

        if website:
            try:
                validate = URLValidator(schemes=('http', 'https'))
                validate(website)
            except Exception as e:
                self.add_error('website',"Invalid Website URL")
        if dob:
            pass

class Contact(forms.Form):
    person = forms.CharField(label="Contact Person", max_length=50, required=True)
    purpose = forms.CharField(label="Contact Type/Purpose (e.g Bookings)",required=True, max_length=50)
    phone = forms.CharField(label="Contact Person's Phone", max_length=15, required=True)
    email = forms.EmailField(label="Contact Person's Email Address", required=True)
    whatsapp = forms.BooleanField(label=_("Phone is on WhatsApp?"), required=False)
    
    def clean(self):
        cleaned_data = super(Contact, self).clean()
        person = cleaned_data.get('person')
        purpose = cleaned_data.get('purpose')
        phone = cleaned_data.get('phone')
        email = cleaned_data.get('email')

        if person:
            if len(person) < 3:
                self.add_error('person', 'Name too short. Try again.')
            elif len(person) > 20:
                self.add_error('person', 'Name too long. Let`s keep it short ;)')
            else:
                regex = re.compile(r'^[a-zA-Z\s]+$', re.U)
                if not regex.match(person):
                    self.add_error('person', 'Please enter a valid name.')
        
        if purpose:
            if len(purpose) < 3:
                self.add_error('purpose', 'Purpose too long. Let`s keep it short ;)')
            elif len(purpose) > 20:
                self.add_error('purpose', 'Purpose too long. Let`s keep it short ;)')
            else:
                regex = re.compile(r'^[a-zA-Z\s]+$', re.U)
                if not regex.match(purpose):
                    self.add_error('purpose', 'Please enter a valid purpose as illustrated.')

        if phone:
            regex = re.compile(r'^\+?1?\d{9,15}$')
            if not regex.match(phone):
                self.add_error('phone', 'Please enter a valid phone number, with country code.')
        
        if email:
            pass