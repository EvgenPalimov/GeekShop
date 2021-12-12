from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
# Create your views here.
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import CreateView

from baskets.models import Basket
from mainapp.mixin import UserDipatchMixin
from mainapp.models import Product

class BasketAddCreateView(CreateView, UserDipatchMixin):
    title = 'GeekShop | Создать продукт'


    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            user_select = request.user
            product = Product.objects.get(id=self.kwargs.get('id'))
            baskets = Basket.objects.filter(user=user_select, product=product)
            if baskets:
                basket = baskets.first()
                basket.quantity += 1
                basket.save()
            else:
                Basket.objects.create(user=user_select, product=product, quantity=1)

            products = Product.objects.all()
            context = {'products': products}
            result = render_to_string('mainapp/includes/card.html', context, request=request)
            return JsonResponse({'result': result})


# @login_required
# def basket_add(request, id):
#     if request.is_ajax():
#         user_select = request.user
#         product = Product.objects.get(id=id)
#         baskets = Basket.objects.filter(user=user_select, product=product)
#         if baskets:
#             basket = baskets.first()
#             basket.quantity += 1
#             basket.save()
#         else:
#             Basket.objects.create(user=user_select, product=product, quantity=1)
#
#         products = Product.objects.all()
#         context = {'products': products}
#         result = render_to_string('mainapp/includes/card.html', context)
#         return JsonResponse({'result': result})


@login_required
def basket_remove(request, basket_id):
    Basket.objects.get(id=basket_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, id_basket, quantity):
    if request.is_ajax():
        basket = Basket.objects.get(id=id_basket)
        basket.quantity = quantity
        basket.save()

        baskets = Basket.objects.filter(user=request.user)
        context = {'baskets': baskets}
        result = render_to_string('baskets/basket.html', context)
        return JsonResponse({'result': result})
