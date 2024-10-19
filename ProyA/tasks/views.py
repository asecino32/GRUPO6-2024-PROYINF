from django.shortcuts import render, redirect
from .models import Usuarios

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'register.html')

def guardar_registro(request):
    usuario = Usuarios(tipo_usuario = 0, nombre_usuario = request.POST['nombre'], password =  request.POST['password'], correo_usuario = request.POST['correo'])
    usuario.save()
    return redirect('/index/login')

def login(request):
    return render(request, 'login.html')