from django.shortcuts import render
import json


# Create your views here.

def index(request):
    content = {
        'title': 'GeekShop', }
    return render(request, 'mainapp/index.html', content)


def products(request):
    with open('mainapp/fixtures/products.json', encoding='utf-8') as f:
        products_list = json.load(f)
    content = {
        'title': 'GeekShop - Каталог',
        'products': products_list,
    }
    return render(request, 'mainapp/products.html', content)

