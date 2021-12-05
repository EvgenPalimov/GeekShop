from django.urls import path

from admins.views import UserTemplateView, UserListView, UserCreateView, UserUpdateView, UserDeleteView, \
    admin_products, admin_products_create, admin_products_update, admin_products_delete, admin_categories, \
    admin_categories_create, admin_categories_update, admin_categories_delete

app_name = 'admins'
urlpatterns = [
    path('', UserTemplateView.as_view(), name='index'),
    path('users/', UserListView.as_view(), name='admin_users'),
    path('users-create/', UserCreateView.as_view(), name='admin_users_create'),
    path('users-update/<int:pk>', UserUpdateView.as_view(), name='admin_users_update'),
    path('users-delete/<int:pk>', UserDeleteView.as_view(), name='admin_users_delete'),
    path('products/', admin_products, name='admin_products'),
    path('products-create/', admin_products_create, name='admin_products_create'),
    path('products-update/<int:pk>', admin_products_update, name='admin_products_update'),
    path('products-delete/<int:pk>', admin_products_delete, name='admin_products_delete'),
    path('categories/', admin_categories, name='admin_categories'),
    path('categories-create/', admin_categories_create, name='admin_categories_create'),
    path('categories-update/<int:pk>', admin_categories_update, name='admin_categories_update'),
    path('categories-delete/<int:pk>', admin_categories_delete, name='admin_categories_delete'),
]
