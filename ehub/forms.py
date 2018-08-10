from django import forms

class SignIn(forms.Form):
    email_address = forms.EmailField(widget=forms.TextInput(attrs={'class':'input-text', 'id':'email'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input-text', 'id':'password'}), max_length=20, required=True)


class SignUp(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'input-text'}), max_length=30, required=True)
    email_address = forms.EmailField(widget=forms.TextInput(attrs={'class':'input-text'}), required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input-text'}), max_length=20, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input-text'}), max_length=20, required=False)