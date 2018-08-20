from django import forms
import re
from utils.models import *
from django.core.validators import URLValidator

su_fo = []

for s in EventPurpose.objects.all():
    su_fo.append([s.id,s])

city_list = []
for c in City.objects.all():
    city_list.append([c.id,c])


class Venue(forms.Form):
    #about
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), required=True)
    suitable = forms.CharField(widget=forms.SelectMultiple(choices=su_fo, attrs={'class':'chosen-select-no-single'}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'WYSIWYG','cols':"40",'rows':"3"}), required=False)
   
    #contacts
    website = forms.URLField(widget=forms.TextInput(attrs={'class':'input-text'}),)
    contact_person = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), max_length=30, required=True)
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), max_length=15, required=True)
    email = forms.EmailField(required=False)
    is_on_whatsapp = forms.BooleanField(required=False)

    #location
    street_address = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}),min_length=5, max_length=70, required=False)
    city = forms.CharField(widget=forms.Select(choices=city_list, attrs={'class':'chosen-select-no-single'}), required=True)
    latitude = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), max_length=30, required=False)
    longitude = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), max_length=30, required=False)
    #images
    main_img = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/*'}), required=True)
    other_img = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/*','multiple':'multiple'}), required=False)
    
    def clean(self):
            data = super(Venue, self).clean()

            name = data.get('name')
            if len(name) < 4:
                self.add_error('name', 'Name too short. Try again.')
            elif len(name) > 200:
                self.add_error('name', 'Name too long. Let`s keep it short ;)')
            else:
                regex = re.compile(r'^[a-zA-Z0-9\s\-\'\w]+$', re.U)
                if not regex.match(name):
                    self.add_error('name', 'Please enter a valid title.')

            # try:
            #     suitable = EventPurpose.objects.get(id=data.get('suitable'))
            # except EventPurpose.DoesNotExist:
            #     self.add_error('suitable', 'Please enter a purpose.')

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
         
            if data.get('street_address'):
                regex = re.compile(r'[a-zA-Z0-9\-\'\w]+')
                if not regex.match(data.get('street_address')):
                    self.add_error('street_address', 'Please enter a valid street address.')

            if data.get('city'):
                try:
                    City.objects.get(id=data.get('city'))
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

            