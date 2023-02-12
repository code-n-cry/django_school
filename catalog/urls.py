from django.urls import path, re_path, register_converter

from . import converters, views

app_name = 'catalog'
register_converter(converters.IntConverter, 'digit')
urlpatterns = [
    path('', views.item_list, name='index'),
    path('<int:number>/', views.item_detail, name='detail'),
    re_path(r'^re/(?P<number>[0-9]+)/', views.item_detail, name='re_detail'),
    path('converter/<digit:number>/', views.item_detail, name='converter_detail'),
]
