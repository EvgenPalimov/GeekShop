from django.contrib import admin

# Register your models here.
from mainapp.models import ProductCategory, Product, CatalogName

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(CatalogName)
