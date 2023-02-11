from django.urls import path, re_path, register_converter
from . import converters, views

register_converter(converters.IntConverter, 'digit')
urlpatterns = [
    path('', views.item_list),
    path('<int:number>/', views.item_detail),
    re_path(r'^re/(?P<number>[0-9]+)/', views.item_detail),
    path('converter/<digit:number>/', views.item_detail),
]
