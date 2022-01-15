from django.urls import path
from django.views.decorators.cache import cache_page

from mainapp.views import CatalogListView, ProductDetail

app_name = 'mainapp'
urlpatterns = [
    path('', CatalogListView.as_view(), name='products'),
    path('category/<int:id_category>', cache_page(3600)(CatalogListView.as_view()), name='category'),
    path('page/<int:page>', cache_page(3600)(CatalogListView.as_view()), name='page'),
    path('detail/<int:pk>/', ProductDetail.as_view(), name='detail'),
]

