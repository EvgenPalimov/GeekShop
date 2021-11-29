from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import ProductCategory, Product
# Create your views here.

def index(request):
    content = {
        'title': 'GeekShop', }
    return render(request, 'mainapp/index.html', content)


def products(request):
    context = {
        'title': 'GeekShop | Каталог',
    }

    # Получение данных из БД
    context['product_category'] = ProductCategory.objects.all()
    context['products'] = Product.objects.all()
    return render(request, 'mainapp/products.html', context)

def detail(request, product_id):
    context = {
        'title': 'GeekShop | Карточка товара', }

    product = Product.objects.filter(id=product_id)
    context['product'] = product

    return render(request, 'mainapp/detail.html', context)