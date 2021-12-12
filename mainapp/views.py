from django.core.paginator import Paginator
from django.views.generic import DetailView, ListView, TemplateView

from .mixin import BaseClassContextMixin
from .models import ProductCategory, Product


# Create your views here.


class IndexTemplateView(TemplateView, BaseClassContextMixin):
    template_name = 'mainapp/index.html'
    title = 'GeekShop'


class CatalogListView(ListView, BaseClassContextMixin):
    model = Product
    template_name = 'mainapp/products.html'
    title = 'GeekShop | Каталог'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CatalogListView, self).get_context_data(**kwargs)

        context['categories'] = ProductCategory.objects.all()
        if self.kwargs:
            products = Product.objects.filter(category_id=self.kwargs.get('id_category')).order_by('name')
        else:
            products = Product.objects.all().order_by('name')
        paginator = Paginator(products, per_page=3)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        context['products'] = page_obj
        return context


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
