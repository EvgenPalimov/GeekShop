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
        'title': 'Geekshop - Каталог',
    }

    # Получение данных из БД
    context['product_category'] = ProductCategory.objects.all()
    context['products'] = Product.objects.all()
    return render(request, 'mainapp/products.html', context)
