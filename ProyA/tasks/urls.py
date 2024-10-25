from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index),
    path('register/', views.register),
    path('new/', views.guardar_registro),
    path('fuente/', views.guardar_fuente),
    path('boletin/', views.consultar_boletin),
    path('login/', login , name="Login"),
    path('check/', views.comprobar_registro),
    path('home/', views.home),
    path('home/subir_boletines', views.subir_boletines),
    path('home/agregar_fuentes', views.agregar_fuentes)
]
