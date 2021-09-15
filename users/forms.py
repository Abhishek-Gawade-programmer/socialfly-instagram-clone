from django import forms

from .models import *

from django.contrib.auth.forms import UserCreationForm
from django.db import transaction


import requests
from django.core import files
from io import BytesIO





class UserSignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)
        del self.fields['password2']
        self.fields['password1'].help_text = None
        self.fields['username'].help_text = None

    username = forms.CharField(label="",max_length=254,widget=forms.TextInput(attrs={"type": "text",'placeholder':'Username'}),required=True)

    password1 = forms.CharField(label="",
        widget=forms.PasswordInput(attrs={"type": "password",'placeholder':'Password'}))


    first_name = forms.CharField(label="",max_length=30,widget=forms.TextInput(attrs={"id":"first-name" ,"type":"text" ,"class":"form__input"  ,"placeholder":"First Name"}),required=True)
    last_name = forms.CharField(label="",max_length=30,widget=forms.TextInput(attrs={"id":"last-name" ,"type":"text" ,"class":"form__input"  ,"placeholder":"Last Name"}),required=True)
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


    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        g=SocialflyUser.objects.filter(phone_number=phone_number)
        if g.exists():
            raise forms.ValidationError('Phone number already registered')
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # if email
        g=User.objects.filter(email=email)
        if g.exists():
            raise forms.ValidationError('Email already registered')
        return email


    class Meta(UserCreationForm.Meta):
        model = User
        exclude = ['password2',]


    @transaction.atomic
    def save(self):  
        user = super().save(commit=False)
        user.first_name=self.cleaned_data.get('first_name')
        user.last_name=self.cleaned_data.get('last_name')
        user.email=self.cleaned_data.get('email')
        user.save()
        socialflyuser = SocialflyUser.objects.create(user=user)
        socialflyuser.phone_number=self.cleaned_data.get('phone_number')
        try:
            url=f'https://ui-avatars.com/api/?name={user.first_name}+{user.last_name}&size=256&bold=true&background=random'
            response = requests.get(url)
            fp = BytesIO()  
            fp.write(response.content)
            socialflyuser.profile_photo.save(user.username+'.png', files.File(fp))
        except :
            pass
        socialflyuser.save()
        return user


class UserEditFrom(forms.ModelForm):
    username = forms.CharField(label="",max_length=254,widget=forms.TextInput(attrs={'id':"user-name",'type':"text" ,'class':"form__input"  ,'placeholder':"Username"}),required=True)
    first_name = forms.CharField(label="",max_length=30,widget=forms.TextInput(attrs={"id":"first-name" ,"type":"text" ,"class":"form__input"  ,"placeholder":"First Name"}),required=True)
    last_name = forms.CharField(label="",max_length=30,widget=forms.TextInput(attrs={"id":"last-name" ,"type":"text" ,"class":"form__input"  ,"placeholder":"Last Name"}),required=True)
    email = forms.EmailField(label="",widget=forms.TextInput(attrs= {"id":"email" ,"type":"email" ,"class":"form__input"  ,"placeholder":"Email"}))
    phone_number = forms.CharField(label="",max_length=10,widget=forms.NumberInput(attrs={'placeholder':'Phone Number'}))
    bio= forms.CharField(label="",max_length=4500,widget=forms.Textarea(attrs={'rows':"3"}))
    birth_date=forms.DateField(label='',widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.CharField(label='',initial='R',max_length=20,widget=forms.Select(choices=GENDER_CHOICES,attrs={'id':"gender",'class':"form-control",'placeholder':"sdfs"}))

    def clean_username(self,*args, **kwargs):
        username = self.cleaned_data.get("username")
        qs=User.objects.filter(username=username)
        if self.instance:
            qs=qs.exclude(pk=self.instance.pk)
        if qs.exists() :
            raise forms.ValidationError(f'({username}) username is already taken try another one')
        return username


    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")

        qs=SocialflyUser.objects.filter(phone_number=phone_number)
        if self.instance:
            qs=qs.exclude(pk=self.instance.pk)
        if qs.exists() :
            raise forms.ValidationError('Phone number already registered')
        return phone_number


    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs=User.objects.filter(email=email)
        if self.instance:
            qs=qs.exclude(pk=self.instance.pk)
        if qs.exists() :
            raise forms.ValidationError('Email already registered')
        return email



    class Meta:
        model=SocialflyUser

        exclude=('followers','following','user')

    
