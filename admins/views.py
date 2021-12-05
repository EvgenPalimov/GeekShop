from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm, ProductAdminRegistrationForm, \
    ProductAdminProfileForm, ProductCategoriesAdminRegistrationForm, ProductCategoriesAdminProfileForm
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
    form_class = UserAdminProfileForm
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


@user_passes_test(lambda u: u.is_superuser)
def admin_products(request):
    products = Product.objects.all()
    context = {
        'title': 'GeekShop - Админ | Продукты',
        'products': products
    }
    return render(request, 'admins/products/admin-products-read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_products_create(request):
    if request.method == 'POST':
        form = ProductAdminRegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_products'))
    else:
        form = ProductAdminRegistrationForm
    context = {
        'title': 'GeekShop - Админ | Создание продукта',
        'form': form
    }
    return render(request, 'admins/products/admin-products-create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_products_update(request, pk):
    product_select = Product.objects.get(pk=pk)

    if request.method == 'POST':
        form = ProductAdminProfileForm(data=request.POST, instance=product_select, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_products'))
    else:
        form = ProductAdminProfileForm(instance=product_select)
    context = {
        'title': 'GeekShop - Админ | Редактирование товара',
        'form': form,
        'product_select': product_select
    }
    return render(request, 'admins/products/admin-products-update-delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_products_delete(request, pk):
    if request.method == 'POST':
        Product.objects.get(pk=pk).delete()
    return HttpResponseRedirect(reverse('admins:admin_products'))


@user_passes_test(lambda u: u.is_superuser)
def admin_categories(request):
    categories = ProductCategory.objects.all()
    context = {
        'title': 'GeekShop - Админ | Категории',
        'categories': categories
    }
    return render(request, 'admins/categories/admin-categories-read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_categories_create(request):
    if request.method == 'POST':
        form = ProductCategoriesAdminRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_categories'))
    else:
        form = ProductCategoriesAdminRegistrationForm
    context = {
        'title': 'GeekShop - Админ | Создание категории',
        'form': form
    }
    return render(request, 'admins/categories/admin-categories-create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_categories_update(request, pk):
    category_select = ProductCategory.objects.get(pk=pk)

    if request.method == 'POST':
        form = ProductCategoriesAdminProfileForm(data=request.POST, instance=category_select)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_categories'))
    else:
        form = ProductCategoriesAdminProfileForm(instance=category_select)
    context = {
        'title': 'GeekShop - Админ | Редактирование категории',
        'form': form,
        'category_select': category_select
    }
    return render(request, 'admins/categories/admin-categories-update-delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_categories_delete(request, pk):
    if request.method == 'POST':
        ProductCategory.objects.get(pk=pk).delete()
    return HttpResponseRedirect(reverse('admins:admin_categories'))
