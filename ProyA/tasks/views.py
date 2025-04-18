import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import FileResponse
from .models import Boletin, Fuente, Comentario


# Create your views here.
def index(request):
    boletines = Boletin.objects.all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para comentar.")
            return redirect('login')
        
        boletin_id = request.POST.get('boletin_id')
        contenido = request.POST.get('contenido')

        boletin = Boletin.objects.get(id_boletin=boletin_id)
        Comentario.objects.create(
            boletin=boletin,
            usuario=request.user,
            contenido=contenido
        )
        messages.success(request, "Comentario publicado correctamente.")
        return redirect('index')

    return render(request, 'index.html', {'boletines': boletines})

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validaciones
        if not username or not email or not password1:
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'register.html')

        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return render(request, 'register.html')

        # Crear el usuario
        user = User(username=username, email=email, password=make_password(password1))
        user.save()

        messages.success(request, 'Tu cuenta ha sido creada exitosamente. Ahora puedes iniciar sesión.')
        login(request, user)  # Inicia sesión automáticamente después del registro
        return redirect('index')  
    return render(request, 'register.html')

def registerStaff_view(request):
    if request.method == 'POST':
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        username = re.split('@', email)[0]
        # Validaciones
        if not firstName or not lastName or not email or not password1:
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'registerStaff.html')

        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'registerStaff')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return render(request, 'registerStaff.html')

        # Crear el usuario
        user = User(username=username, first_name=firstName, last_name=lastName, email=email, password=make_password(password1), is_staff=True)
        user.save()

        messages.success(request, 'Tu cuenta ha sido creada exitosamente. Ahora puedes iniciar sesión.')
        login(request, user)  # Inicia sesión automáticamente después del registro
        return redirect('home')  
    return render(request, 'registerStaff.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Autenticar usuario
        user = authenticate(request, username=username, password=password)
        # if user is None:
        #     user = authenticate(request, email=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido, {username}!')
            return redirect('index') 
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
            return render(request, 'login.html')

    return render(request, 'login.html')

def loginStaff_view(request):
    if request.method == 'POST':
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        password = request.POST.get('password')

        try: # Buscar al usuario por nombre y apellido
            user = User.objects.get(first_name=firstName, last_name=lastName)
        except User.DoesNotExist:
            user = None
        if user.is_staff == False:
            user = None
            messages.error(request, 'No se encontró un usuario con ese nombre y apellido.')
            return render(request, 'loginStaff.html')
        if user:
            # Autenticar con username y password
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido, {firstName}!')
                return redirect('home')
            else:
                messages.error(request, 'Contraseña incorrecta.')
        else:
            messages.error(request, 'No se encontró un usuario con ese nombre y apellido.')

        return render(request, 'loginStaff.html')

    return render(request, 'loginStaff.html')

def home_view(request):
    if request.user.is_authenticated:
        return render(request, 'home.html', {'usuario': request.user})
    else:
        return render(request, 'login.html') 

def logout_view(request):
    logout(request) 
    return redirect('index')

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

def subir_boletines_view(request):
    return render(request, 'subir_boletines.html')

def guardar_boletines_view(request):
    if request.method == 'POST':
        archivo_pdf = request.FILES.get('archivo_pdf')  # Captura el archivo PDF
        titulo_boletin=request.POST['titulo']
        fuente_boletin = request.POST['fuente']
        if not archivo_pdf:  # Verifica que el archivo PDF sea obligatorio
            messages.error(request, 'El archivo PDF es obligatorio.')
            return redirect('subir_boletines')
        if not titulo_boletin:
            messages.error(request, 'El titulo del boletin es obligatorio.')
            return redirect('subir_boletines')
        if not fuente_boletin:
            messages.error(request, 'La fuente del boletin es obligatoria.')
            return redirect('subir_boletines')
        
        boletin = Boletin(
            titulo=titulo_boletin,
            ciudad_tratada=request.POST['ciudad_tratada'],
            tematica=request.POST['tematica'],
            fuente_boletin_id = fuente_boletin,
            archivo=archivo_pdf
        )
        boletin.save()

        messages.success(request, 'Boletín subido con éxito.')
        return redirect('subir_boletines')

def guardar_fuente_view(request):
    if request.method == 'POST':
        titulo_fuente=request.POST['titulo']
        
        if not titulo_fuente:
            messages.error(request, 'El titulo de la fuente es obligatorio.')
            return redirect('agregar_fuentes')
            
        fuente = Fuente(
            titulo = titulo_fuente, 
            descripcion= request.POST['descripcion'] , 
            fuente_activa = 1, 
            url = request.POST['url']
        )
        fuente.save()
        messages.success(request, 'Fuente subida con éxito.')
        return redirect('agregar_fuentes')
    
def eliminar_boletin_view(request):
    return render(request, 'eliminar_boletin.html')

def del_boletin_view(request):
    boletin = Boletin(id_boletin = request.POST['id'])
    boletin.delete()
    messages.success(request, 'Se elimino exitosamente el boletin.')
    return redirect('eliminar_boletin')




def agregar_fuentes_view(request):
    return render(request, 'agregar_fuentes.html')

def ver_boletin(request, boletin_id):
    # Obtén el boletín desde la base de datos
    boletin = get_object_or_404(Boletin, id_boletin=boletin_id)

    # Obtén el archivo PDF asociado al boletín
    archivo_path = boletin.archivo.path

    # Devuelve el archivo como respuesta para ser visualizado en el navegador
    return FileResponse(open(archivo_path, 'rb'), content_type='application/pdf')

def consultar_boletin(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        ciudad_tratada = request.POST.get('ciudad_tratada', '').strip()
        tematica = request.POST.get('tematica', '').strip()
        fecha = request.POST.get('fecha', '').strip()

        consulta = Q()
        if titulo:
            consulta &= Q(titulo__icontains=titulo)
        if ciudad_tratada:
            consulta &= Q(ciudad_tratada__icontains=ciudad_tratada)
        if tematica:
            consulta &= Q(tematica__icontains=tematica)
        if fecha:
            try:
                fecha_inicio = datetime.strptime(fecha, '%Y-%m-%d').date()

                fecha_actual = datetime.now().date()

                consulta &= Q(fecha_creacion__range=(fecha_inicio, fecha_actual))
            except ValueError:
                pass

        resultados = Boletin.objects.filter(consulta)

        return render(request, 'home.html', {'resultados': resultados})

    return redirect('/index/home')


def ver_fuente(request, fuente_id):
    # Obtener el objeto Fuente usando el ID
    fuente = get_object_or_404(Fuente, id_fuente=fuente_id)
    
    # Renderizar el template con los detalles del objeto
    return render(request, 'ver_fuente.html', {'fuente': fuente})