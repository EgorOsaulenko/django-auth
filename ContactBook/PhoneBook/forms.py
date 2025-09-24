from django import forms
from .models import Contact




class ContactForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}), label="Ім'я")
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}), label="Прізвище")
    email = forms.EmailField(max_length=50, required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}), label="Електронна пошта")
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}), label="Номер телефону")
    address = forms.CharField(max_length=255, required=False, widget=forms.Textarea(attrs={'class': 'form-control'}), label="Адреса")
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={"class": "form-control"}), label="Фотографія профіля")

    class Meta:
        model = Contact
        fields = ("first_name", "last_name", "email", "phone_number", "address", "profile_picture")


        #update