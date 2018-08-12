from django import forms
from utils.models import City, Tag
import base64

city_list = []
for c in City.objects.all():
    city_list.append([c.id,c])

tags = []
for t in Tag.objects.all():
    tags.append([t.id, t.name])


class Profile(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), max_length=30, required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'input-text'}), required=False)
    handle = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), max_length=30, required=True)
    city = forms.CharField(widget=forms.Select(choices=city_list, attrs={'class':'chosen-select-no-single'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), max_length=15, required=False)
    tags = forms.CharField(widget=forms.SelectMultiple(choices=tags, attrs={'class':'chosen-select-no-single','placeholder':'Select tags'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'cols':'30','rows':'10'}), required=False)

class Avatar(forms.Form):
    update_avatar = forms.CharField(widget=forms.HiddenInput(), required=True)
    base64image = forms.CharField(widget=forms.HiddenInput(), required=True)

    def clean(self):
        cleaned_data = super(Avatar, self).clean()
        update_avatar = cleaned_data.get('update_avatar')
        
        if update_avatar != '1':
            self.add_error('update_avatar', 'Action Unauthorized')
        
