from django.urls import path

from ordersapp.views import OrderList, OrderDelete, OrderCreate, OrderDetail, \
    OrderUpdate, order_forming_complete, \
    get_product_price, payment_result

app_name = 'ordersapp'
urlpatterns = [
    path('', OrderList.as_view(), name='list'),
    path('create/', OrderCreate.as_view(), name='create'),
    path('update/<int:pk>/', OrderUpdate.as_view(), name='update'),
    path('read/<int:pk>/', OrderDetail.as_view(), name='read'),
    path('delete/<int:pk>/', OrderDelete.as_view(), name='delete'),
    path('forming_complete/<int:pk>/', order_forming_complete,
         name='forming_complete'),
    path('product/<int:pk>/price/', get_product_price,
         name='get_product_price'),
    path('payment/result/', payment_result, name='payment_result')
]
