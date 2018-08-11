from django import forms
import re

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
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

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
        
        