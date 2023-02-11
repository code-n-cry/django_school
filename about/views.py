from django.http import HttpResponse


def description(request):
    return HttpResponse('<body>Об этом проекте говорить ещё нечего:(</body>')
