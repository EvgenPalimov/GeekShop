from django.shortcuts import render

# Create your views here.
def login(request):
    content = {
        'title': 'GeekShop | �����������', }
    return render(request, 'authapp/login.html', content)

def registration(request):
    content = {
        'title': 'GeekShop | �����������', }
    return render(request, 'authapp/registration.html', content)