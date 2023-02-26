from django.http import HttpResponse
from django.shortcuts import render


def item_list(request):
    template = 'catalog/item_list.html'
    context = {'title': 'Каталог'}
    return render(request, template, context)


def item_detail(request, number):
    return HttpResponse(f'<body>Элемент {number} - красивый, нужный.</body>')
