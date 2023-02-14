from http import HTTPStatus

from django.http import HttpResponse


def home(request):
    return HttpResponse('<body>Главная страница O_o</body>')


def coffee(request):
    return HttpResponse(
        'Я чайник', content_type='text/plain', status=HTTPStatus.IM_A_TEAPOT)
