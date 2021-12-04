from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm, ProductAdminRegistrationForm, \
    ProductAdminProfileForm, ProductCategoriesAdminRegistrationForm, ProductCategoriesAdminProfileForm
from authapp.models import User
from mainapp.models import Product, ProductCategory


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render(request, 'admins/admin.html')


@user_passes_test(lambda u: u.is_superuser)
def admin_users(request):
    context = {
        'title': 'GeekShop - Админ',
        'users': User.objects.all()
    }
    return render(request, 'admins/admin-users-read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_users_create(request):
    if request.method == 'POST':
        form = UserAdminRegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_users'))
    else:
        form = UserAdminRegistrationForm
    context = {
        'title': 'GeekShop - Админ | Регистрация',
        'form': form
    }
    return render(request, 'admins/admin-users-create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_users_update(request, pk):
    user_select = User.objects.get(pk=pk)

    if request.method == 'POST':
        form = UserAdminProfileForm(data=request.POST, instance=user_select, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_users'))
    else:
        form = UserAdminRegistrationForm(instance=user_select)
    context = {
        'title': 'GeekShop - Админ | Редактирование',
        'form': form,
        'user_select': user_select
    }
    return render(request, 'admins/admin-users-update-delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_users_delete(request, pk):
    if request.method == 'POST':
        user = User.objects.get(pk=pk)
        if user.is_active == True:
            user.is_active = False
            user.save()
        else:
            user.is_active = True
            user.save()

    return HttpResponseRedirect(reverse('admins:admin_users'))


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
