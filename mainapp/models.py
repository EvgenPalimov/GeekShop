from django.core.validators import FileExtensionValidator, validate_image_file_extension
from django.db import models

import os

# Create your models here.
from authapp.models import MaxSizeValidator


class ProductCategory(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to='product_image', blank=True, validators=[MaxSizeValidator(2)])
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} | {self.category}'
