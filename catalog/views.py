import datetime
import random

import django.db.models
import django.shortcuts
import django.utils
from django.utils.translation import gettext_lazy
from django.views.generic import DetailView, ListView

import catalog.models


class ItemListView(ListView):
    template_name = 'catalog/item_list.html'
    queryset = catalog.models.Item.objects.published()
    context_object_name = 'items'
    http_method_names = ['get', 'head']


class ItemDetailView(DetailView):
    template_name = 'catalog/item_detail.html'
    queryset = catalog.models.Item.objects.published()
    http_method_names = ['get', 'head']


class HaveNeverChangedView(ListView):
    template_name = 'catalog/extra_item_list.html'
    queryset = catalog.models.Item.objects.published().filter(
        created_at=django.db.models.F(
            catalog.models.Item.updated_at.field.name
        )
    )
    context_object_name = 'items'
    extra_context = {
        'title': gettext_lazy('Непроверенное'),
        'header': gettext_lazy(
            'Товары, ни разу не менявшиеся с момента добавления'
        ),
    }
    http_method_names = ['get', 'head']


class AddedLastWeek(HaveNeverChangedView):
    queryset = catalog.models.Item.objects.published().filter(
        created_at=django.db.models.F(
            catalog.models.Item.updated_at.field.name
        )
    )
    context_object_name = 'items'
    extra_context = {
        'title': gettext_lazy('Непроверенное'),
        'header': gettext_lazy(
            'Товары, ни разу не менявшиеся с момента добавления'
        ),
    }
    ids = catalog.models.Item.objects.filter(is_published=True).values_list(
        catalog.models.Item.id.field.name, flat=True
    )
    queryset = None
    if ids:
        amount = 5
        if len(ids) < 5:
            amount = len(ids)
        queryset = (
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
    extra_context = {
        'title': gettext_lazy('Новинки'),
        'header': gettext_lazy('Пять товаров, добавленных на этой неделе'),
    }
    http_method_names = ['get', 'head']


class EditedAtAnyFridayView(HaveNeverChangedView):
    ids = catalog.models.Item.objects.published().values_list(
        catalog.models.Item.id.field.name, flat=True
    )
    queryset = None
    context_object_name = 'items'
    if ids:
        queryset = catalog.models.Item.objects.filter(
            updated_at__week_day=6,
            id__in=list(ids)[-1:-6],
        )
    extra_context = {
        'title': gettext_lazy('Пятница'),
        'header': gettext_lazy(
            'Последние пять товаров, изменённых в любую пятницу'
        ),
    }
    http_method_names = ['get', 'head']
