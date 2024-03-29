from django.db import transaction
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, \
    DeleteView, DetailView
from django.shortcuts import get_object_or_404, redirect

from baskets.models import Basket
from mainapp.mixin import BaseClassContextMixin, UserDipatchMixin
from mainapp.models import Product
from ordersapp.forms import OrderItemsForm
from ordersapp.models import Order, OrderItem


class OrderList(ListView, BaseClassContextMixin, UserDipatchMixin):
    model = Order
    title = 'GeekShop | Список заказов'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user,
                                    is_active=True).select_related()


class OrderCreate(CreateView, BaseClassContextMixin, UserDipatchMixin):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:list')
    title = 'GeekShop | Создание заказа'

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data(**kwargs)

        OrderFormSet = inlineformset_factory(Order, OrderItem,
                                             form=OrderItemsForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST)

        else:
            basket_item = Basket.objects.filter(
                user=self.request.user).select_related()
            if basket_item:
                OrderFormSet = inlineformset_factory(Order, OrderItem,
                                                     form=OrderItemsForm,
                                                     extra=basket_item.count())
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_item[num].product
                    form.initial['quantity'] = basket_item[num].quantity
                    form.initial['price'] = basket_item[num].product.price
                basket_item.delete()
            else:
                formset = OrderFormSet()
        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            if self.object.get_total_cost == 0:
                self.object.delete()
        return super(OrderCreate, self).form_valid(form)


class OrderUpdate(UpdateView, BaseClassContextMixin, UserDipatchMixin):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:list')
    title = 'GeekShop | Обновление заказа'

    def get_context_data(self, **kwargs):
        context = super(OrderUpdate, self).get_context_data(**kwargs)

        OrderFormSet = inlineformset_factory(Order, OrderItem,
                                             form=OrderItemsForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price

        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
        return super(OrderUpdate, self).form_valid(form)


class OrderDelete(DeleteView, BaseClassContextMixin):
    model = Order
    success_url = reverse_lazy('orders:list')
    title = 'GeekShop | Удаление заказа'


class OrderDetail(DetailView, BaseClassContextMixin, UserDipatchMixin):
    model = Order
    title = 'GeekShop | Чтение заказа'


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SEND_TO_PROCEED
    order.save()
    return redirect(reverse_lazy('ordersapp:read', kwargs={'pk': pk}))


def get_product_price(request, pk):
    if request.is_ajax():
        product = Product.objects.get(pk=pk)
        if product:
            return JsonResponse({'price': product.price})
        return JsonResponse({'price': 0})


@receiver(pre_save, sender=Basket)
def product_quantity_save(sender, instance, **kwargs):
    if instance.pk:
        instance.product.quantity -= instance.quantity - instance.get_item(
            int(instance.pk))
    else:
        instance.product.quantity -= instance.quantity
        instance.product.save()


@receiver(pre_delete, sender=Basket)
def product_quantity_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()


def payment_result(request):
    status = request.GET.get('ik_inv_st')
    if status == 'success':
        order_pk = request.GET.get('ik_pm_no')
        order_item = Order.objects.get(pf=order_pk)
        order_item.status = Order.PAID
        order_item.save()
    return HttpResponseRedirect(reverse('ordersapp:list'))
