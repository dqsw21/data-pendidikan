from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('dashboard/', views.home, name='home'),
    path('dataset/', views.dataset_explorer, name='dataset'),
    path('prediksi/', views.prediction_page, name='prediction'),
]

urlpatterns += [
    path('informasi-model/', views.model_info_page, name='model_info'),
    path('tentang/', views.about_page, name='about'),
]

urlpatterns += [
    path('dashboard-ai/', views.dashboard_ai_explanation, name='dashboard_ai'),
]

urlpatterns += [
    path('prediction-ai/', views.prediction_ai_explanation, name='prediction_ai'),
]

urlpatterns += [
    path('province-chart-ai/', views.province_chart_ai, name='province_chart_ai'),
]
