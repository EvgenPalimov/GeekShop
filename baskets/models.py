from django.db import models
from django.utils.functional import cached_property

from authapp.models import User
from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    create_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | ' \
               f'Продукт {self.product.name}'

    @cached_property
    def get_item_cached(self):
        return self.user.basket.select_related()

    def sum(self):
        return self.quantity * self.product.price

    def total_sum(self):
        baskets = self.get_item_cached
        return sum(basket.sum() for basket in baskets)

    def total_quantity(self):
        baskets = self.get_item_cached
        return sum(basket.quantity for basket in baskets)

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk).quantity
