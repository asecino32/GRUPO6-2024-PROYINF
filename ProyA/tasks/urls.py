from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index),
    path('register/', views.register),
    path('new/', views.guardar_registro),
    path('login/', login , name="Login"),
    path('check/', views.comprobar_registro),
    path('home/', views.home)
]
