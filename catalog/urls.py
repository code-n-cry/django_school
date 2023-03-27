from django.urls import path, re_path, register_converter

from catalog import converters, views

app_name = "catalog"
register_converter(converters.IntConverter, "positive")
urlpatterns = [
    path("", views.ItemListView.as_view(), name="item_list"),
    path("<int:pk>/", views.ItemDetailView.as_view(), name="item_detail"),
    path(
        "friday/",
        views.EditedAtAnyFridayView.as_view(),
        name="edited_at_friday",
    ),
    path("novelties/", views.AddedLastWeek.as_view(), name="added_last_week"),
    path(
        "unchecked/",
        views.HaveNeverChangedView.as_view(),
        name="have_never_changed",
    ),
    re_path(
        r"^re/(?P<pk>[1-9]\d*)/$",
        views.ItemDetailView.as_view(),
        name="regex_item_detail",
    ),
    path(
        "converter/<positive:number>/",
        views.ItemDetailView.as_view(),
        name="converter_item_detail",
    ),
]
