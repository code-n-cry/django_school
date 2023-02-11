from django.http import HttpResponse


def home(request):
    return HttpResponse('<body><h1>Главная страница O_o</h1></body>')
