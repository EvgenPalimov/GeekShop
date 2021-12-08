from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from authapp.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from authapp.models import User
from baskets.models import Basket
from mainapp.mixin import BaseClassContextMixin, UserDipatchMixin


class UserLoginView(LoginView, BaseClassContextMixin):
    model = User
    template_name = 'authapp/login.html'
    form_class = UserLoginForm
    title = 'GeekShop | Авторизация'


class UserShopCreateView(CreateView, BaseClassContextMixin):
    model = User
    template_name = 'authapp/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('authapp:login')
    title = 'GeekShop | Создать пользователя'


class UserShopUpdateView(UpdateView, BaseClassContextMixin, SuccessMessageMixin):
    model = User
    template_name = 'authapp/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('authapp:profile')
    title = 'Админ | Редактирование пользователя'
    success_message = "%(calculated_field)s was created successfully"

    def get_success_message(self, cleaned_data):
        self.object = self.get_object()
        if self.object.is_valid():
            return self.success_message % dict(
                cleaned_data,
                calculated_field=self.object.calculated_field,
            )
        else:
            return self.object.errors


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.set_level(request, messages.SUCCESS)
#             messages.success(request, 'Данные успешно сохранены!')
#         else:
#             messages.set_level(request, messages.ERROR)
#             messages.error(request, form.errors)
#
#     context = {
#         'title': 'GeekShop | Профайл',
#         'form': UserProfileForm(instance=request.user),
#         'baskets': Basket.objects.filter(user=request.user)
#     }
#     return render(request, 'authapp/profile.html', context)

class UserLogoutView(LogoutView, BaseClassContextMixin):
    model = User
    template_name = 'mainapp/index.html'
    success_url = reverse_lazy('index')
    title = 'GeekShop | Выход'

# def logout(request):
#     auth.logout(request)
#     return render(request, 'mainapp/index.html')
