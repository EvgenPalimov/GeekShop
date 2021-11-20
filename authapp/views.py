from django.shortcuts import render

# Create your views here.
def login(request):
    content = {
        'title': 'GeekShop | Авторизация', }
    return render(request, 'authapp/login.html', content)

def registration(request):
    content = {
        'title': 'GeekShop | Регистрация', }
    return render(request, 'authapp/registration.html', content)