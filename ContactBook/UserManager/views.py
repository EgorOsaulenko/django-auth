from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest
from django.db import IntegrityError

from .forms import SignUpForm, LoginForm


def sign_up(request):
    if request.user.is_authenticated:
        return redirect("store_home")
    
    form = SignUpForm(data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            try:
                user = form.save()
                login(request=request, user=user)
                messages.add_message(request=request, level=messages.SUCCESS, message="Ви зарєєструвались.")
                return redirect("store_home")
            except IntegrityError as e:
                # Обробка помилки унікальності (наприклад, якщо username вже існує)
                if 'username' in str(e):
                    form.add_error('username', 'Користувач з таким іменем вже існує. Будь ласка, оберіть інше ім\'я.')
                    messages.add_message(request=request, level=messages.ERROR, 
                                       message="Користувач з таким іменем вже існує. Будь ласка, оберіть інше ім'я.")
                else:
                    messages.add_message(request=request, level=messages.ERROR, 
                                       message="Помилка при реєстрації. Спробуйте ще раз.")
    
    return render(request=request, template_name="sign_up.html", context={"form": form})


def sign_in(request):
    if request.user.is_authenticated:
        return redirect("store_home")
    
    form = LoginForm(data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            username=form.cleaned_data.get("username"),
            password=form.cleaned_data.get("password")
        )
        if user:
            login(request=request, user=user)
            messages.add_message(request=request, level=messages.SUCCESS, message="Ви війшли в аккаунт.")
            return redirect("store_home")
        else:
            messages.add_message(request=request, level=messages.ERROR, message="Помилка.")
            
    return render(request=request, template_name="sign_in.html", context=dict(form=form))
    

@login_required(login_url="/sign_in/")
def index(request):
    return render(request=request, template_name="index.html")


def logout_func(request):
    logout(request)
    messages.success(request, "Ви успішно вийшли")
    return redirect("sign_in")