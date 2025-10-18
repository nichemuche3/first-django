from django.urls import path
from . import views

urlpatterns = [
    path('', views.bus_stations, name='bus_stations'),
    path('stations/', views.bus_stations, name='bus_stations'),  # альтернативный путь
]