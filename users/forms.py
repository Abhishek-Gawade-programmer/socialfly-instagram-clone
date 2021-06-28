from django.contrib.auth.forms import AuthenticationForm

from django import forms


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(widget=forms.TextInput(
        attrs={'name':'username','placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'name':'password','placeholder':'Password','class':'mt-3'}))