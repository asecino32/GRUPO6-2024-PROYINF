import re, tempfile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import FileResponse, HttpResponse
from .models import Boletin, Fuente, Comentario, PlantillaBoletin
from django.contrib.auth.decorators import login_required
from .forms import PlantillaBoletinForm, CrearBoletinForm
from django.core.files import File
from io import BytesIO
from django.core.files.base import ContentFile
from django.template import Context, Template
from weasyprint import HTML
from django.utils import timezone


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
        codigo = request.POST.get('codigo')
        username = request.POST.get('email')
        # Validaciones
        
        if not firstName or not lastName or not email or not password1 or not codigo:
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'registerStaff.html')
        
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'registerStaff')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return render(request, 'registerStaff.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return render(request, 'registerStaff.html')
        
        if codigo != 'FIA2025':
            messages.error(request, 'Codigo incorrecto.')
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
        if not firstName or not lastName or not password:
            messages.error(request, 'Debes completar todos los campos.')
            return render(request, 'loginStaff.html')

        try: # Buscar al usuario por nombre y apellido
            user = User.objects.get(first_name=firstName, last_name=lastName)
        except User.DoesNotExist:
            user = None
        if user != None:
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

@login_required
def home_view(request):
    if not request.user.is_staff:
        return HttpResponse("Acceso denegado", status=403)
    elif request.user.is_authenticated:
        return render(request, 'home.html', {'usuario': request.user})
    else:
        return render(request, 'login.html') 

def logout_view(request):
    logout(request) 
    return redirect('index')

""" def filtrar_boletines(request):
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
            try:
                fecha_obj = datetime.strptime(fecha_creacion, '%Y-%m-%d').date()
                boletines = boletines.filter(fecha_creacion=fecha_obj)
            except ValueError:
                pass  # Podrías manejar errores de formato si lo deseas

    # Renderizar la plantilla 'home.html' y pasar los boletines filtrados
    return render(request, 'home.html', {'boletines': boletines})
 """
@login_required
def subir_boletines_view(request):
    if not request.user.is_staff:
        return HttpResponse("Acceso denegado", status=403)
    else:
        return render(request, 'subir_boletines.html')

@login_required
def guardar_boletines_view(request):
    if not request.user.is_staff:
        return HttpResponse("Acceso denegado", status=403)
    
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

@login_required
def guardar_fuente_view(request):
    if not request.user.is_staff:
        return HttpResponse("Acceso denegado", status=403)
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
    
    if not request.user.is_staff:
        return HttpResponse("Acceso denegado", status=403)
    else:
        return render(request, 'eliminar_boletin.html')

@login_required
def del_boletin_view(request):
    if not request.user.is_staff:
        return HttpResponse("Acceso denegado", status=403)
    boletin = Boletin(id_boletin = request.POST['id'])
    boletin.delete()
    messages.success(request, 'Se elimino exitosamente el boletin.')
    return redirect('eliminar_boletin')

@login_required
def agregar_fuentes_view(request):
    if not request.user.is_staff:
        return HttpResponse("Acceso denegado", status=403)
    else:
        return render(request, 'agregar_fuentes.html')


@login_required
def consultar_boletin(request):
    if not request.user.is_staff:
        return HttpResponse("Acceso denegado", status=403)
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

def ver_boletin(request, boletin_id):
    # Obtén el boletín desde la base de datos
    boletin = get_object_or_404(Boletin, id_boletin=boletin_id)

    # Obtén el archivo PDF asociado al boletín
    archivo_path = boletin.archivo.path

    # Devuelve el archivo como respuesta para ser visualizado en el navegador
    return FileResponse(open(archivo_path, 'rb'), content_type='application/pdf')


""" @login_required
def crear_boletin(request):
    if not request.user.is_staff:
        return HttpResponse("Acceso denegado", status=403)

    plantillas = PlantillaBoletin.objects.all()

    if request.method == 'POST':
        plantilla_id = request.POST.get('plantilla_id')
        contenido_personalizado = request.POST.get('contenido')
        plantilla = get_object_or_404(PlantillaBoletin, id=plantilla_id)

        # Aquí podrías guardar el boletín creado en la base de datos si lo deseas

        contenido_final = plantilla.contenido_html.replace("{{contenido}}", contenido_personalizado)

        return render(request, 'ver_boletin.html', {
            'contenido_final': contenido_final,
        })

    return render(request, 'crear_boletin.html', {
        'plantillas': plantillas
    })
    """

@login_required
def subir_plantilla(request):
    if not request.user.is_staff:
        return HttpResponse("Acceso denegado", status=403)

    if request.method == 'POST':
        form = PlantillaBoletinForm(request.POST, request.FILES)
        if form.is_valid():
            plantilla = form.save(commit=False)
            
            archivo_html = request.FILES.get('archivo_html')
            if archivo_html:
                contenido = archivo_html.read().decode('utf-8')
                plantilla.contenido_html = contenido

            plantilla.save()
            return redirect('crear_boletin')
    else:
        form = PlantillaBoletinForm()
    
    return render(request, 'subir_plantilla.html', {'form': form})

@login_required
def crear_boletin(request):
    if not request.user.is_staff:
        return HttpResponse("Acceso denegado", status=403)

    if request.method == 'POST':
        form = CrearBoletinForm(request.POST)
        if form.is_valid():
            boletin = form.save(commit=False)
            plantilla = form.cleaned_data['plantilla']
            contenido_editor = form.cleaned_data['contenido_html']

            # Pre-formatear todas las variables (incluyendo el año)
            contexto = {
                'titulo': boletin.titulo,
                'ciudad_tratada': boletin.ciudad_tratada,
                'tematica': boletin.tematica,
                'fuente_url': boletin.fuente_boletin.url if boletin.fuente_boletin else '#',
                'fecha_creacion': timezone.now().strftime('%Y-%m-%d'),  # Fecha completa
                'ano_actual': timezone.now().strftime('%Y'),  # Solo el año
                'contenido_editor': contenido_editor,
            }

            if plantilla:
                contenido_final = plantilla.contenido_html
                
                # Reemplazar variables (incluyendo el año)
                contenido_final = contenido_final.replace('{{ titulo }}', contexto['titulo'])
                contenido_final = contenido_final.replace('{{ ciudad_tratada }}', contexto['ciudad_tratada'])
                contenido_final = contenido_final.replace('{{ tematica }}', contexto['tematica'])
                contenido_final = contenido_final.replace('{{ fuente_boletin }}', contexto['fuente_url'])
                contenido_final = contenido_final.replace('{{ fecha_creacion }}', contexto['fecha_creacion'])
                contenido_final = contenido_final.replace('{{ fecha_creacion|date:"Y" }}', contexto['ano_actual'])  # Filtro de año
                
                # Reemplazar contenido editable
                contenido_final = re.sub(
                    r'<!-- CONTENIDO_EDITABLE_INICIO -->.*?<!-- CONTENIDO_EDITABLE_FIN -->',
                    f'<!-- CONTENIDO_EDITABLE_INICIO -->{contenido_editor}<!-- CONTENIDO_EDITABLE_FIN -->',
                    contenido_final,
                    flags=re.DOTALL
                )
            else:
                contenido_final = f"""
                <!DOCTYPE html>
                <html>
                <body>
                    <!-- Encabezado -->
                    <h1>{contexto['titulo']}</h1>
                    <p>Fecha: {contexto['fecha_creacion']} (Año: {contexto['ano_actual']})</p>
                    
                    <!-- Contenido -->
                    <div class="contenido">{contexto['contenido_editor']}</div>
                    
                    <!-- Pie de página -->
                    <footer>© {contexto['ano_actual']}</footer>
                </body>
                </html>
                """

            # Generar PDF (el resto del código se mantiene igual)
            pdf_buffer = BytesIO()
            HTML(string=contenido_final).write_pdf(pdf_buffer)
            pdf_buffer.seek(0)
            
            boletin.archivo.save(f'boletin_{datetime.now().strftime("%Y%m%d%H%M%S")}.pdf', ContentFile(pdf_buffer.read()))
            boletin.save()
            return redirect('home')
    else:
        form = CrearBoletinForm()

    return render(request, 'crear_boletin.html', {'form': form})