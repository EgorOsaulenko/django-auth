from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}), label="Ім'я")
    last_name = forms.CharField(max_length=70, widget=forms.TextInput(attrs={"class": "form-control"}), label="Прізвище")
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={"class": "form-control"}), label="Номер телефону")
    email = forms.EmailField(max_length=40, required=False, widget=forms.TextInput(attrs={"class": "form-control"}), label="Ємайл")
    address = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={"class": "form-control"}), label="Адреса")
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={"class": "form-control"}), label="Аватарка")
    
    class Meta:
        model = Contact
        fields = ("first_name", "last_name", "phone_number", "email", "address", "profile_picture",)