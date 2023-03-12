from django.urls import path, re_path, register_converter

from catalog import converters, views

app_name = 'catalog'
register_converter(converters.IntConverter, 'positive')
urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('friday/', views.edited_at_any_friday, name='edited_at_friday'),
    path('novelties/', views.added_last_week, name='added_last_week'),
    path('unchecked/', views.have_never_changed, name='have_never_changed'),
    path('<int:number>/', views.item_detail, name='item_detail'),
    re_path(
        r'^re/(?P<number>[1-9]\d*)/$',
        views.item_detail,
        name='regex_item_detail',
    ),
    path(
        'converter/<positive:number>/',
        views.item_detail,
        name='converter_item_detail',
    ),
]
