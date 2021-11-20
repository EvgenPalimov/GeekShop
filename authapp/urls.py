from django.urls import path
from authapp.views import login, registration, logout

app_name = 'authapp'
urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('logout/', logout, name='logout'),
]
