import datetime
import random

import django.db.models
import django.shortcuts
import django.utils

import catalog.models


def item_list(request):
    template = 'catalog/item_list.html'
    items = catalog.models.Item.objects.published()
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


def have_never_changed(request):
    template = 'catalog/extra_item_list.html'
    items = catalog.models.Item.objects.filter(
        created_at=django.db.models.F(
            catalog.models.Item.updated_at.field.name
        )
    )
    title = 'Непроверенное'
    header = 'Товары, ни разу не менявшиеся с момента добавления'
    context = {'items': items, 'title': title, 'header': header}
    return django.shortcuts.render(request, template, context)


def added_last_week(request):
    template = 'catalog/extra_item_list.html'
    ids = catalog.models.Item.objects.filter(is_published=True).values_list(
        catalog.models.Item.id.field.name, flat=True
    )
    items = None
    if ids:
        amount = 5
        if len(ids) < 5:
            amount = len(ids)
        items = (
            catalog.models.Item.objects.published()
            .filter(
                id__in=random.sample(list(ids), k=amount),
                created_at__range=[
                    django.utils.timezone.now() - datetime.timedelta(weeks=1),
                    django.utils.timezone.now(),
                ],
            )
            .order_by('?')
        )
    title = 'Новинки'
    header = 'Пять товаров, добавленных на этой неделе'
    context = {'items': items, 'title': title, 'header': header}
    return django.shortcuts.render(request, template, context)


def edited_at_any_friday(request):
    template = 'catalog/extra_item_list.html'
    ids = catalog.models.Item.objects.published().values_list(
        catalog.models.Item.id.field.name, flat=True
    )
    items = None
    if ids:
        items = catalog.models.Item.objects.filter(
            updated_at__week_day=6,
            id__in=list(ids)[-1:-6],
        )
    title = 'Пятница'
    header = 'Последние пять товаров, изменённых в любую пятницу'
    context = {'items': items, 'title': title, 'header': header}
    return django.shortcuts.render(request, template, context)
