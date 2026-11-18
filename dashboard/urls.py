from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dataset/', views.dataset_explorer, name='dataset'),
]
