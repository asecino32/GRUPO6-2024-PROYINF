from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register/', views.register),
    path('new/', views.guardar_registro),
    path('login/', views.login),
    path('check/', views.comprobar_registro),
    path('home/', views.home)
]
