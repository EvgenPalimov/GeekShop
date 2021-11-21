

from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from authapp.forms import UserLoginForm, UserRegistrationForm


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('mainapp:products'))
        else:
            print(form.errors)
    else:
        form = UserLoginForm()
    content = {
        'title': 'GeekShop | Авторизация',
        'form': form
    }
    return render(request, 'authapp/login.html', content)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('authapp:login'))
        else:
            print(form.errors)
    else:
        form = UserRegistrationForm()
    content = {
        'title': 'GeekShop | Регистрация',
        'form': form
    }
    return render(request, 'authapp/registration.html', content)

def logout(request):
    auth.logout(request)
    return render(request, 'mainapp/index.html')
