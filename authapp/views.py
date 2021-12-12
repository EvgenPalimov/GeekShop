from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

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

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            messages.set_level(request, messages.SUCCESS)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return HttpResponseRedirect(reverse('authapp:login'))
        else:
            messages.set_level(request, messages.ERROR)
            messages.error(request, form.errors)
        return render(request, self.template_name, {'form': form})


class UserShopUpdateView(UpdateView, BaseClassContextMixin, UserDipatchMixin):
    template_name = 'authapp/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('authapp:profile')
    title = 'GeekShop - Профиль'

    def form_valid(self, form):
        messages.set_level(self.request, messages.SUCCESS)
        messages.success(self.request, "Данные успешно сохранены!")
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, *args, **kwargs):
        return get_object_or_404(User, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super(UserShopUpdateView, self).get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context


class UserLogoutView(LogoutView, BaseClassContextMixin):
    template_name = 'mainapp/index.html'
    title = 'GeekShop | Выход'
