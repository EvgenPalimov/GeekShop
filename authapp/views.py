from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from authapp.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from baskets.models import Basket


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
            messages.success(request, 'Поздравляем, вы успешно зарегистрировались!')
            return HttpResponseRedirect(reverse('authapp:login'))
    else:
        form = UserRegistrationForm()
    content = {
        'title': 'GeekShop | Регистрация',
        'form': form
    }
    return render(request, 'authapp/registration.html', content)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.set_level(request, messages.SUCCESS)
            messages.success(request, 'Данные успешно сохранены!')
        else:
            messages.set_level(request, messages.ERROR)
            messages.error(request, form.errors)

    content = {
        'title': 'GeekShop | Профайл',
        'form': UserProfileForm(instance=request.user),
        'baskets': Basket.objects.filter(user=request.user)
    }
    return render(request, 'authapp/profile.html', content)


def logout(request):
    auth.logout(request)
    return render(request, 'mainapp/index.html')
