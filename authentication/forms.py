from django import forms
import re
from .models import *

class SignIn(forms.Form):
    email_address = forms.EmailField(widget=forms.TextInput(attrs={'class':'input-text', 'id':'email'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input-text', 'id':'password'}), max_length=20, required=True)


class SignUp(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), max_length=30, required=True)
    email_address = forms.EmailField(widget=forms.TextInput(attrs={'class':'input-text'}), required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input-text'}), max_length=20, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input-text'}), max_length=20, required=False)

    def clean(self):
        cleaned_data = super(SignUp, self).clean()
        name = cleaned_data.get('name')
        email_address = cleaned_data.get('email_address')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        #email validation
        if User.objects.filter(email=email_address).count() > 0:
              self.add_error('email_address', 'Email already in use.')

        #Name validation
        if not len(name.split()) > 1:
            self.add_error('name', 'Please enter full name.')
        elif len(name.split()) > 2:
            self.add_error('name', 'Please enter only first and last names.')
        else:
            regex = re.compile(r'^[a-zA-Z]{2,}[\s][a-zA-Z]{2,}$', re.U)
            if not regex.match(name):
                self.add_error('name', 'Please enter a valid name.')

        #Password Validation
        if len(password) < 6:
            self.add_error('password', 'Passwords must be at least 6 characters.')
        elif len(password) > 20:
            self.add_error('password', 'Password too long, we recomment 10 - 20 characters.')
        elif password != confirm_password:
            self.add_error('password', 'The passwords you entered do not match.')
        
class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input-text'}), max_length=20, required=True)
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input-text'}), max_length=20, required=True)
    verify_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input-text'}), max_length=20, required=True)

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        new = cleaned_data.get('new_password')
        verify = cleaned_data.get('verify_password')

        if len(new) < 6:
            self.add_error('new_password', 'Password too short.')
        elif new != verify:
            self.add_error('new_password', 'Passwords do not match.')
            self.add_error('verify_password', 'Passwords do not match.')


        

