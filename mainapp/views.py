from django.shortcuts import render
from django.views.generic import DetailView

from .models import ProductCategory, Product


# Create your views here.

def index(request):
    content = {
        'title': 'GeekShop',
    }
    return render(request, 'mainapp/index.html', content)


def products(request, id_category=None):
    context = {
        'title': 'GeekShop | Каталог'
    }

    context['categories'] = ProductCategory.objects.all()
    if id_category:
        context['products'] = Product.objects.filter(category_id=id_category)
    else:
        context['products'] = Product.objects.all()
    # Получение данных из БД
    return render(request, 'mainapp/products.html', context)


class ProductDetail(DetailView):
    """
    Контроллер вывода информации о продукте
    """
    model = Product
    template_name = 'mainapp/detail.html'

    def get_context_data(self, **kwargs):
        """Добавляем список категории для вывода сайдбара с катеногриями на странице каталога"""
        context = super(ProductDetail, self).get_context_data(**kwargs)
        product = self.get_object()
        context['product'] = product
        return context
