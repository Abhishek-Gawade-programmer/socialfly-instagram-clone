from django import forms

from .models import *

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

class UserSignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)
        del self.fields['password2']
        self.fields['password1'].help_text = None
        self.fields['username'].help_text = None

    username = forms.CharField(label="",max_length=254,widget=forms.TextInput(attrs={"type": "text",'placeholder':'Username'}),required=True)

    password1 = forms.CharField(label="",
        widget=forms.PasswordInput(attrs={"type": "password",'placeholder':'Password'}))


    first_name = forms.CharField(label="",max_length=30,widget=forms.TextInput(attrs={"type": "text",'placeholder':'First Name'}),required=True)
    last_name = forms.CharField(label="",max_length=30,widget=forms.TextInput(attrs={"type": "text",'placeholder':'Last Name'}),required=True)
    email = forms.EmailField(label="",widget=forms.TextInput(attrs={"type": "email",'placeholder':'Email'}))


    phone_number = forms.CharField(label="",max_length=10,
        widget=forms.NumberInput(attrs={'placeholder':'Phone Number'}))
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    class Meta(UserCreationForm.Meta):
        model = User
        exclude = ['password2',]

    @transaction.atomic
    def save(self):  
        print(self.cleaned_data)
        user = super().save(commit=False)
        user.first_name=self.cleaned_data.get('first_name')
        user.last_name=self.cleaned_data.get('last_name')
        user.email=self.cleaned_data.get('email')
        user.save()
        socialflyuser = SocialflyUser.objects.create(user=user)
        socialflyuser.phone_number=self.cleaned_data.get('phone_number')
        socialflyuser.save()
        return user


class UserEditFrom(forms.ModelForm):
    username = forms.CharField(label="",max_length=254,widget=forms.TextInput(attrs={"type": "text",'placeholder':'Username'}),required=True)

    password1 = forms.CharField(label="",
        widget=forms.PasswordInput(attrs={"type": "password",'placeholder':'Password'}))
    class Meta:
        model=SocialflyUser

        exclude=('followers','following','user')

        widgets = {
               'birth_date': forms.widgets.DateInput(attrs={'type': 'date'}),

     

        }

