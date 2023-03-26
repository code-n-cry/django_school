from django.urls import path

from about import views

app_name = 'about'
urlpatterns = [
    path('', views.DescriptionView.as_view(), name='description'),
    path('thanks/', views.ThanksForFeedbackView.as_view(), name='thanks'),
]
