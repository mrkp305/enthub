from django import forms

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
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('password', 'The passwords you entered do not match')