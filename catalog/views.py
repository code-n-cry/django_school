import django.shortcuts

import catalog.models


def item_list(request):
    template = 'catalog/item_list.html'
    items = catalog.models.Item.objects.published().order_by('category__name')
    context = {'items': items}
    return django.shortcuts.render(request, template, context)


def item_detail(request, number):
    template = 'catalog/item_detail.html'
    item = django.shortcuts.get_object_or_404(
        catalog.models.Item,
        pk=number,
    )
    context = {'item': item}
    return django.shortcuts.render(request, template, context)
