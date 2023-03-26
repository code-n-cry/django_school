import datetime
import random

import django.db.models
import django.shortcuts
import django.utils
from django.utils.translation import gettext_lazy
from django.views.generic import TemplateView

import catalog.models


class ItemListView(TemplateView):
    template_name = 'catalog/item_list.html'
    items = catalog.models.Item.objects.published()
    extra_context = {'items': items}


class ItemDetailView(TemplateView):
    template_name = 'catalog/item_detail.html'

    def get(self, request, number, *args, **kwargs):
        item = django.shortcuts.get_object_or_404(
            catalog.models.Item,
            pk=number,
        )
        context = self.get_context_data(**kwargs)
        context.update({'item': item})
        return self.render_to_response(context)


class HaveNeverChangedView(TemplateView):
    template_name = 'catalog/extra_item_list.html'

    def get(self, request, *args, **kwargs):
        items = catalog.models.Item.objects.filter(
            created_at=django.db.models.F(
                catalog.models.Item.updated_at.field.name
            )
        )
        title = gettext_lazy('Непроверенное')
        header = gettext_lazy(
            'Товары, ни разу не менявшиеся с момента добавления'
        )
        extra_context = {'items': items, 'title': title, 'header': header}
        context = self.get_context_data(**kwargs)
        context.update(extra_context)
        return self.render_to_response(context)


class AddedLastWeek(HaveNeverChangedView):
    def get(self, request, *args, **kwargs):
        ids = catalog.models.Item.objects.filter(
            is_published=True
        ).values_list(catalog.models.Item.id.field.name, flat=True)
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
                        django.utils.timezone.now()
                        - datetime.timedelta(weeks=1),
                        django.utils.timezone.now(),
                    ],
                )
                .order_by('?')
            )
        title = gettext_lazy('Новинки')
        header = gettext_lazy('Пять товаров, добавленных на этой неделе')
        exatra_context = {'items': items, 'title': title, 'header': header}
        context = self.get_context_data(**kwargs)
        context.update(exatra_context)
        return self.render_to_response(context)


class EditedAtAnyFridayView(HaveNeverChangedView):
    def get(self, request, *args, **kwargs):
        ids = catalog.models.Item.objects.published().values_list(
            catalog.models.Item.id.field.name, flat=True
        )
        items = None
        if ids:
            items = catalog.models.Item.objects.filter(
                updated_at__week_day=6,
                id__in=list(ids)[-1:-6],
            )
        title = gettext_lazy('Пятница')
        header = gettext_lazy(
            'Последние пять товаров, изменённых в любую пятницу'
        )
        extra_context = {'items': items, 'title': title, 'header': header}
        context = self.get_context_data(**kwargs)
        context.update(extra_context)
        return self.render_to_response(context)
