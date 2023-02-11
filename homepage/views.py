from django.http import HttpResponse


def home(request):
    return HttpResponse('<body>Главная страница O_o</body>')


def coffee(request):
    response = HttpResponse('Я чайник', content_type='text/plain')
    response.status_code = 418
    return response
