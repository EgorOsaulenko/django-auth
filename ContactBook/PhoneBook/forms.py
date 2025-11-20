from django import forms

from .models import Contact, Product


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


class ProductForm(forms.ModelForm):
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Назва товару"
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        label="Опис"
    )
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        label="Ціна"
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"}),
        label="Зображення"
    )
    is_new = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Новий товар"
    )
    rating = forms.IntegerField(
        min_value=0,
        max_value=5,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Рейтинг (0-5)"
    )
    count = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Кількість на складі"
    )
    
    class Meta:
        model = Product
        fields = ("name", "description", "price", "image", "is_new", "rating", "count",)