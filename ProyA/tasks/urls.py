from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', login_view,  name='login'),
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),

    path('home/subir_boletines', views.subir_boletines_view, name='subir_boletines'),
    path('save_boletin/', views.guardar_boletines_view, name='save_boletin'),
    path('home/agregar_fuentes', views.agregar_fuentes_view, name='agregar_fuentes'),
    path('save_fuente/', views.guardar_fuente_view, name='save_fuente'),
    path('home/eliminar_boletin', views.eliminar_boletin_view,name='eliminar_boletin'),
    path('del_boletin/', views.del_boletin_view,name='del_boletin'),

    path('boletin/', views.consultar_boletin),
    path('ver_fuente/<int:fuente_id>/', views.ver_fuente, name='ver_fuente'),
    
    
]
