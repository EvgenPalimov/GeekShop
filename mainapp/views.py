from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView

from .mixin import BaseClassContextMixin, CustomDispatchMixin
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


# def products(request, id_category=None, page=1):
#     context = {
#         'title': 'GeekShop | Каталог'
#     }
#
#     if id_category:
#         products = Product.objects.filter(category_id=id_category)
#     else:
#         products = Product.objects.all()
#
#     paginator = Paginator(products, per_page=3)
#
#     try:
#         products_paginator = paginator.page(page)
#     except PageNotAnInteger:
#         products_paginator = paginator.page(1)
#     except EmptyPage:
#         products_paginator = paginator.page(paginator.num_pages)
#
#     context['products'] = products_paginator
#     context['categories'] = ProductCategory.objects.all()
#     return render(request, 'mainapp/products.html', context)


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
