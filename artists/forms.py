'''
    Django Imports
'''
from django import forms
'''
    End Django Imports
'''

'''
    Other Model Imports
'''
from utils.models import *
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
for genre in Genre.objects.all():
    genres.append([genre.pk,genre])

class DateInput(forms.DateInput):
    input_type = 'date'

class Profile(forms.Form):

    stage_name = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), max_length=30, required=True)
    genre = forms.CharField(widget=forms.Select(choices=genres, attrs={'class':'chosen-select-no-single'}))
    alias = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), max_length=30, required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'class':'input-text'}))
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'class':'input-text', 'type':'date'}))

    def clean(self):
        cleaned_data = super(Profile, self).clean()
        stage_name = cleaned_data.get('stage_name')
        genre = cleaned_data.get('genre')
        alias = cleaned_data.get('alias')
        dob = cleaned_data.get('dob')

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

        if dob:
            pass

    