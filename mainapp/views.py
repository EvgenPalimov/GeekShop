from django.shortcuts import render


# Create your views here.

def index(request):
    content = {
        'title': 'Geekshop', }

    return render(request, 'mainapp/index.html', content)


def products(request):
    content = {
        'title': 'GeekShop - Каталог', }
    return render(request, 'mainapp/products.html', content)
