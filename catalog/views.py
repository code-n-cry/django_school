import datetime
import random

import django.db.models
import django.shortcuts
import django.utils
from django.utils.translation import gettext_lazy
from django.views.generic import DetailView, ListView

import catalog.models
import rating.forms
import rating.models


class ItemListView(ListView):
    template_name = "catalog/item_list.html"
    queryset = catalog.models.Item.objects.published()
    context_object_name = "items"
    http_method_names = ["get", "head"]


RATING_DONT_EXIST_VALUE = 0


class ItemDetailView(DetailView):
    rating_form_class = rating.forms.RatingForm
    template_name = "catalog/item_detail.html"
    queryset = catalog.models.Item.objects.published().prefetch_related(
        django.db.models.Prefetch(
            rating.models.Rating.rating.field.name,
            queryset=rating.models.Rating.objects.all(),
        )
    )
    model = catalog.models.Item
    http_method_names = ["get", "post", "head"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ratings = context["item"].rating.all()
        context["rating_avg"] = sum(
            map(lambda x: x.rating or 0, ratings)
        ) / len(ratings)

        context["rating_form"] = self.rating_form_class()
        ratings_map_users = list(map(lambda x: x.user_id, ratings))
        context["user_rating"] = RATING_DONT_EXIST_VALUE
        if self.request.user.is_authenticated:
            if self.request.user.pk in ratings_map_users:
                rating_idx = ratings_map_users.index(self.request.user.pk)
                user_rating = ratings[rating_idx]
                if user_rating.rating is None:
                    user_rating = RATING_DONT_EXIST_VALUE
                context["user_rating"] = user_rating
                context["rating_form"] = self.rating_form_class(
                    instance=user_rating
                )
        return context

    def post(self, request, *args, **kwargs):
        rating_form = self.rating_form_class(request.POST or None)
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        user_rating = context["user_rating"]
        if rating_form.is_valid() and request.user.is_authenticated:
            if user_rating != RATING_DONT_EXIST_VALUE:
                user_rating.rating = rating_form.cleaned_data["rating"]
                user_rating.save()
            else:
                rating.models.Rating.objects.create(
                    rating=rating_form.cleaned_data["rating"],
                    item=self.object,
                    user=request.user,
                )
        # delete rating button
        if (
            "delete" in request.POST
            and request.user.is_authenticated
            and user_rating != RATING_DONT_EXIST_VALUE
        ):
            user_rating.delete()
            catalog.models.Item.objects
        return django.shortcuts.redirect(
            "catalog:item_detail", pk=kwargs.get("pk")
        )


class HaveNeverChangedView(ListView):
    template_name = "catalog/extra_item_list.html"
    queryset = catalog.models.Item.objects.published().filter(
        created_at=django.db.models.F(
            catalog.models.Item.updated_at.field.name
        )
    )
    context_object_name = "items"
    extra_context = {
        "title": gettext_lazy("Непроверенное"),
        "header": gettext_lazy(
            "Товары, ни разу не менявшиеся с момента добавления"
        ),
    }
    http_method_names = ["get", "head"]


class AddedLastWeek(HaveNeverChangedView):
    queryset = catalog.models.Item.objects.published().filter(
        created_at=django.db.models.F(
            catalog.models.Item.updated_at.field.name
        )
    )
    context_object_name = "items"
    extra_context = {
        "title": gettext_lazy("Непроверенное"),
        "header": gettext_lazy(
            "Товары, ни разу не менявшиеся с момента добавления"
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
            .order_by("?")
        )
    extra_context = {
        "title": gettext_lazy("Новинки"),
        "header": gettext_lazy("Пять товаров, добавленных на этой неделе"),
    }
    http_method_names = ["get", "head"]


class EditedAtAnyFridayView(HaveNeverChangedView):
    ids = catalog.models.Item.objects.published().values_list(
        catalog.models.Item.id.field.name, flat=True
    )
    queryset = None
    context_object_name = "items"
    if ids:
        queryset = catalog.models.Item.objects.filter(
            updated_at__week_day=6,
            id__in=list(ids)[-1:-6],
        )
    extra_context = {
        "title": gettext_lazy("Пятница"),
        "header": gettext_lazy(
            "Последние пять товаров, изменённых в любую пятницу"
        ),
    }
    http_method_names = ["get", "head"]
