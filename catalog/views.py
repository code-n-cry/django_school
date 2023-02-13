from django.http import HttpResponse


def item_list(request):
    return HttpResponse('<body>Список элементов</body>')


def item_detail(request, number):
    return HttpResponse(f'<body>Элемент {number} - красивый, нужный.</body>')
