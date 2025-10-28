from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import SignUp, Login

# Create your views here.
def sign_up(request):
    form = SignUp(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request=request, user=user)
        messages.add_message(request=request, level=messages.SUCCESS, message='Реєстрація пройшла успішно')
        return redirect('index')
    
    return render(request,'sign_up.html', context={'form': form})

def sign_in(request):
    form = Login(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password')
                )
        if user:
            login(request=request, user=user)
            messages.add_message(request=request, level=messages.SUCCESS, message='Вхід пройшов успішно')
            return redirect('index')
        else:
            messages.add_message(request=request, level=messages.ERROR, message='Невірний логін або пароль')
    
    return render(request=request,template_name='sign_in.html', context=dict(form=form))


@login_required(login_url='/users/sign_in')
def index(request):
    return render(request=request, template_name='index.html')