from django.http import HttpResponse


def item_list(request):
    return HttpResponse('<body>Список:<ul><li>Элемент 1</li></ul></body>')


def item_detail(request, number: int):
    return HttpResponse(f'<body>Элемент {number}: красивый, нужный.</body>')
