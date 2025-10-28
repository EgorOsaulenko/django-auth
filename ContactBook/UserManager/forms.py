from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms


class SignUp(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1', 'password2',]


class Login(AuthenticationForm):
    username = forms.CharField(label='Логін')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)