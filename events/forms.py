from django import forms
from utils.models import EventType, City, Country, Genre
from django.core.validators import URLValidator

import re

type_list = []
for t in EventType.objects.all():
    type_list.append([t.id,t])

city_list = []
for c in City.objects.all():
    city_list.append([c.id,c])

class DateInput(forms.DateTimeInput):
    input_type = 'date'

class EventForm(forms.Form):
    #about
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), required=True)
    type = forms.CharField(widget=forms.Select(choices=type_list, attrs={'class':'chosen-select-no-single'}), required=False)
    about = forms.CharField(widget=forms.Textarea(attrs={'class':'WYSIWYG','cols':"40",'rows':"3"}), required=False)
    admission = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), required=False)
    #time/dates
    start_date = forms.DateField(widget=forms.DateTimeInput(attrs={'class':'input-text', 'type':'date'}), required=True)
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'class':'input-text', 'type':'time'}), required=True)
    end_date = forms.DateField(widget=forms.DateTimeInput(attrs={'class':'input-text', 'type':'date'}), required=True)
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'class':'input-text', 'type':'time'}), required=True)
    recurring = forms.BooleanField(required=False)
    #contacts
    website = forms.URLField(widget=forms.TextInput(attrs={'class':'input-text'}),)
    contact_person = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), max_length=30, required=True)
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), max_length=15, required=True)
    email = forms.EmailField(required=False)
    is_on_whatsapp = forms.BooleanField(required=False)
    #location
    location_name = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}),min_length=3, max_length=70, required=True)
    street_address = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}),min_length=5, max_length=70, required=False)
    zip_code = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), max_length=70, required=False)
    city = forms.CharField(widget=forms.Select(choices=city_list, attrs={'class':'chosen-select-no-single'}), required=True)
    latitude = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), max_length=30, required=False)
    longitude = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), max_length=30, required=False)
    #images
    main_poster = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/*'}), required=True)
    other_images = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/*','multiple':'multiple'}), required=False)
    
    def clean(self):
            data = super(EventForm, self).clean()

            title = data.get('title')
            if len(title) < 4:
                self.add_error('title', 'Title too short. Try again.')
            elif len(title) > 20:
                self.add_error('title', 'Title too long. Let`s keep it short ;)')
            else:
                regex = re.compile(r'^[a-zA-Z0-9\s\-\'\w]+$', re.U)
                if not regex.match(title):
                    self.add_error('title', 'Please enter a valid title.')

            try:
                type = EventType.objects.get(id=data.get('type'))
            except EventType.DoesNotExist:
                self.add_error('type', 'Please enter a event type.')

            if data.get('website'):
                try:
                    validate = URLValidator(schemes=('http', 'https'))
                    validate(data.get('website'))
                except Exception as e:
                    self.add_error('website',"Invalid Website URL")            

            if data.get('contact_person'):
                if len(data.get('contact_person')) < 3:
                    self.add_error('contact_person', 'Name too short. Try again.')
                elif len(data.get('contact_person')) > 20:
                    self.add_error('contact_person', 'Name too long. Let`s keep it short ;)')
                else:
                    regex = re.compile(r'^[a-zA-Z\s]+$', re.U)
                    if not regex.match(data.get('contact_person')):
                        self.add_error('contact_person', 'Please enter a valid name.')

            if data.get('phone'):
                regex = re.compile(r'^\+?1?\d{9,15}$')
                if not regex.match(data.get('phone')):
                    self.add_error('phone', 'Please enter a valid phone number, with country code.')
            
            if data.get('location_name'):
                regex = re.compile(r'[a-zA-Z0-9\-\'\w]+')
                if not regex.match(data.get('location_name')):
                    self.add_error('location_name', 'Please enter a valid location name.')

            if data.get('street_address'):
                regex = re.compile(r'[a-zA-Z0-9\-\'\w]+')
                if not regex.match(data.get('street_address')):
                    self.add_error('street_address', 'Please enter a valid street address.')

            if data.get('city'):
                try:
                    type = City.objects.get(id=data.get('city'))
                except City.DoesNotExist:
                    self.add_error('city', 'Please select a valid city.')

            if data.get('zip_code'):
                regex = re.compile(r'[a-zA-Z0-9\-\'\w]+')
                if not regex.match(data.get('zip_code')):
                    self.add_error('zip_code', 'Please enter a valid zip code.')

            if data.get('latitude'):
                regex = re.compile(r'[0-9\,\.\-]+')
                if not regex.match(data.get('latitude')):
                    self.add_error('latitude', 'Please enter valid latitude.')

            if data.get('longitude'):
                regex = re.compile(r'[0-9\,\.\-]+')
                if not regex.match(data.get('longitude')):
                    self.add_error('latitude', 'Please enter valid longitude.')

            



            
