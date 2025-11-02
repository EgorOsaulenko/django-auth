from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.models import User
from .models import MySuperUser
from django import forms 


class  SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={"class": "form-control"}), 
        label="Логін",
        help_text="Введіть імя користувача, максимум 50 символів"
    )
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}), label="Ім'я")
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}), label="Прізвище")
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={"class": "form-control"}), label="Номер телефону")
    adress = forms.CharField(max_length=750, required=False, widget=forms.TextInput(attrs={"class": "form-control"}), label="Адреса")
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Введіть пароль")
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Повторіть пароль")

    class Meta:
        model = MySuperUser
        fields = ("username", "first_name", "last_name", "phone_number", "adress", "password1", "password2",)
        
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Логін", widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    