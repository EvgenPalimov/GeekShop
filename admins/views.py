from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm, ProductAdminRegistrationForm, \
    ProductAdminProfileForm, CategoryUpdateFormAdmin
from authapp.models import User
from mainapp.mixin import CustomDispatchMixin, BaseClassContextMixin
from mainapp.models import Product, ProductCategory


class UserTemplateView(TemplateView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin.html'


class UserListView(ListView, CustomDispatchMixin, BaseClassContextMixin):
    model = User
    template_name = 'admins/admin-users-read.html'
    title = 'Админ | Пользователи'


class UserCreateView(CreateView, CustomDispatchMixin, BaseClassContextMixin):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegistrationForm
    success_url = reverse_lazy('admins:admin_users')
    title = 'Админ | Создать пользователя'


class UserUpdateView(UpdateView, CustomDispatchMixin, BaseClassContextMixin):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')
    title = 'Админ | Редактирование пользователя'


class UserDeleteView(DeleteView, CustomDispatchMixin, BaseClassContextMixin):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    success_url = reverse_lazy('admins:admin_users')
    title = 'Админ | Удаление пользователя'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductsListView(ListView, CustomDispatchMixin, BaseClassContextMixin):
    model = Product
    template_name = 'admins/products/admin-products-read.html'
    title = 'Админ | Продукты'


class ProductCreateView(CreateView, CustomDispatchMixin, BaseClassContextMixin, SuccessMessageMixin):
    model = Product
    template_name = 'admins/products/admin-products-create.html'
    form_class = ProductAdminRegistrationForm
    success_url = reverse_lazy('admins:admin_products')
    success_message = "%(name)s was created successfully"
    title = 'Админ | Создать продукт'



class ProductUpdateView(UpdateView, CustomDispatchMixin, BaseClassContextMixin):
    model = Product
    template_name = 'admins/products/admin-products-update-delete.html'
    form_class = ProductAdminProfileForm
    success_url = reverse_lazy('admins:admin_products')
    title = 'Админ | Редактирование товар'


class ProductDeleteView(DeleteView, CustomDispatchMixin, BaseClassContextMixin):
    model = Product
    template_name = 'admins/products/admin-products-update-delete.html'
    success_url = reverse_lazy('admins:admin_products')
    title = 'Админ | Удаление товара'



class CategoriesListView(ListView, CustomDispatchMixin, BaseClassContextMixin):
    model = ProductCategory
    template_name = 'admins/categories/admin-categories-read.html'
    title = 'Админ | Категории'


class CategoriesCreateView(CreateView, CustomDispatchMixin, BaseClassContextMixin, SuccessMessageMixin):
    model = ProductCategory
    template_name = 'admins/categories/admin-categories-create.html'
    form_class = CategoryUpdateFormAdmin
    success_url = reverse_lazy('admins:admin_categories')
    title = 'Админ | Создать категорию'
    success_message = "%(name)s was created successfully"


class CategoriesUpdateView(UpdateView, CustomDispatchMixin, BaseClassContextMixin):
    model = ProductCategory
    template_name = 'admins/categories/admin-categories-update.html'
    form_class = CategoryUpdateFormAdmin
    success_url = reverse_lazy('admins:admin_categories')
    title = 'Админ | Редактирование категории'


class CategoriesDeleteView(DeleteView, CustomDispatchMixin, BaseClassContextMixin):
    model = ProductCategory
    template_name = 'admins/categories/admin-categories-read.html'
    success_url = reverse_lazy('admins:admin_categories')
    title = 'Админ | Удаление категории'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
