from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import NumberInput

# from App_Login.models import UserProfile

class CreateNewUser(UserCreationForm):
    email = forms.EmailField(required=True, label="",
    widget=forms.TextInput(attrs={'placeholder':'Your Email'}))
    username = forms.CharField(required=True, label="",
    widget=forms.TextInput(attrs={'placeholder':'Your Username'}))
    password1 = forms.CharField(
    required = True,
    label = "",
    widget = forms.PasswordInput(attrs={'placeholder':'Password'})
    )
    password2 = forms.CharField(
    required = True,
    label = "",
    widget = forms.PasswordInput(attrs={'placeholder':'Password Confirmation'})
    )

    class Meta:
        model = User
        fields = ('email','username','password1','password2')


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label="",
    widget=forms.TextInput(attrs={'placeholder':'Your Username'}))
    password = forms.CharField(
    required = True,
    label = "",
    widget = forms.PasswordInput(attrs={'placeholder':'Password'})
    )

class ImageForm(forms.ModelForm):
    class Meta:
        model = Tasveer
        fields = ('name', 'your_image', 'your_say')
        widgets = {'your_say':forms.Textarea(attrs={'rows':3,'cols':20}),}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {'text':forms.Textarea(attrs={'rows':3, 'cols':20, 'placeholder':'your comment here'}),}
