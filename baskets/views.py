from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
# Create your views here.

from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from baskets.models import Basket
from mainapp.mixin import UserDipatchMixin, BaseClassContextMixin
from mainapp.models import Product


class BasketAddCreateView(UpdateView, UserDipatchMixin, BaseClassContextMixin):
    model = Basket
    template_name = 'mainapp/products.html'
    title = 'GeekShop | Добавление товара в корзину!'

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

        messages.set_level(request, messages.SUCCESS)
        messages.success(request, 'Товар успешно добавлен в корзину!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # products = self.object
        # context = {'products': products}
        # result = render_to_string('mainapp/includes/card.html', context, request=request)
        # return JsonResponse({'result': result})


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


@login_required
def basket_remove(request, basket_id):
    Basket.objects.get(id=basket_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
