from django.urls import path
from authapp.views import registration, login

app_name = 'authapp'
urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
]
