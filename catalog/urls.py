from django.urls import path, re_path, register_converter

from . import converters, views

app_name = 'catalog'
register_converter(converters.IntConverter, 'digit')
urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('<int:number>/', views.item_detail, name='item_detail'),
    re_path(r'^re/(?P<number>[1-9]\d*)/', views.item_detail, name='re_detail'),
    path(
        'converter/<digit:number>/', views.item_detail, name='converter_detail'
    ),
]
