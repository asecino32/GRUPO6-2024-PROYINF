from django.shortcuts import render, redirect
from .models import Usuarios
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'register.html')

def guardar_registro(request):
    hashed_password = make_password(request.POST['password'])
    usuario = Usuarios(tipo_usuario = 0, nombre_usuario = request.POST['nombre'], password= hashed_password ,correo_usuario = request.POST['correo'])
    usuario.save()
    return redirect('/index/login')

def login(request):
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def comprobar_registro(request):
    nombre = request.POST.get('nombre')
    correo = request.POST.get('nombre')
    contra = request.POST.get('password')
    print(contra)
    try:
        usuario = Usuarios.objects.get(Q(nombre_usuario=nombre) | Q(correo_usuario=correo))
        
        if check_password(contra, usuario.password):
            return redirect('/index/home')
        else:
            # Contraseña incorrecta
            print("Contraseña incorrecta")
            return redirect('/index/login')

    except Usuarios.DoesNotExist:
        print("Usuario o Correo no estan registrados")
        return redirect('/index/login')