from django.urls import path
from mainapp.views import products, detail

app_name = 'mainapp'
urlpatterns = [
    path('', products, name='products'),
    path('detail/<int:product_id>/', detail, name='detail'),
]

