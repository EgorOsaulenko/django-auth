from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.models import User
from .models import MySuperUser
from django import forms


class SignUp(UserCreationForm):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"class": "form-control"}), label="Логін", help_text="Обов'язково. До 20 символів. Латинські літери, цифри тільки.")
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"class": "form-control"}), label="Ім'я")
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"class": "form-control"}), label="Прізвище")
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={"class": "form-control"}), label="Номер телефону", required=False)
    address = forms.CharField(max_length=500, widget=forms.TextInput(attrs={"class": "form-control"}), label="Адреса", required=False)
    password1 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Пароль")
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Підтвердження пароля")

    class Meta:
        model = MySuperUser
        fields = ("username", "first_name", "last_name", "phone_number", "address", "password1", "password2",)


class Login(AuthenticationForm):
    username = forms.CharField(label="Логін", widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"}))