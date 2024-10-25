from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuarios, Boletin, Fuente
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from django.contrib.auth.decorators import login_required

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

#@login_required
def home(request):
    return render(request, 'home.html')

""" def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html', {'usuario': request.user})
    else:
        return render(request, 'login.html') 
"""

def comprobar_registro(request):
    nombre = request.POST.get('nombre_usuario')
    correo = request.POST.get('nombre_usuario')
    contra = request.POST.get('password')
    print(contra)
    try:
        usuario = Usuarios.objects.get(Q(nombre_usuario=nombre) | Q(correo_usuario=correo))
        
        if check_password(contra, usuario.password):
            print("Usuario valido")
            return redirect('/index/home')
        else:
            # Contraseña incorrecta
            print("Contraseña incorrecta")
            return redirect('/index/login')

    except Usuarios.DoesNotExist:
        print("Usuario o Correo no estan registrados")
        return redirect('/index/login')
    

def filtrar_boletines(request):
    boletines = Boletin.objects.all()  # Obtener todos los boletines como punto de partida
    
    # Filtrar boletines si se ha enviado el formulario
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        ciudad_tratada = request.POST.get('ciudad_tratada')
        tematica = request.POST.get('tematica')
        fecha_creacion = request.POST.get('fecha_creacion')

        # Aplicar los filtros solo si los campos tienen valores
        if titulo:
            boletines = boletines.filter(titulo__icontains=titulo)
        if ciudad_tratada:
            boletines = boletines.filter(ciudad_tratada__icontains=ciudad_tratada)
        if tematica:
            boletines = boletines.filter(tematica__icontains=tematica)
        if fecha_creacion:
            boletines = boletines.filter(fecha_creacion=fecha_creacion)

    # Renderizar la plantilla 'home.html' y pasar los boletines filtrados
    return render(request, 'home.html', {'boletines': boletines})

def subir_boletines(request):
    return render(request, 'subir_boletines.html')

def agregar_fuentes(request):
    return render(request, 'agregar_fuentes.html')

def guardar_fuente(request):
    fuente = Fuente(titulo = request.POST['titulo'], descripcion= request.POST['descripcion'] , fuente_activa = 1, url = request.POST['url'])
    fuente.save()
    messages.success(request, 'Fuente subida con éxito.')
    return redirect('/index/home/agregar_fuentes')

def consultar_boletin(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        ciudad_tratada = request.POST['ciudad_tratada']
        tematica = request.POST['tematica']

        resultados = Boletin.objects.filter(
            titulo=titulo,
            ciudad_tratada=ciudad_tratada,
            tematica=tematica
        )

        return render(request, 'home.html', {'resultados': resultados})

    # Si no es POST, simplemente redirigir o mostrar un formulario vacío
    return redirect('/index/home')