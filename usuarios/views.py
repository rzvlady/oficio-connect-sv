from .forms import ClientProfileForm, WorkerProfileForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from servicios.models import WorkerProfile, ClientProfile

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'usuarios/login.html', {'error': 'Usuario o contraseña incorrectos'})
    return render(request, 'usuarios/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from servicios.models import JobRequest # Asegúrate de importar el modelo

@login_required(login_url='login')
def home_view(request):
    context = {}
    
    # 1. Caso: Cliente
    if hasattr(request.user, 'client_profile'):
        template_name = 'usuarios/home_cliente.html'
    
    # 2. Caso: Trabajador
    elif hasattr(request.user, 'worker_profile') or hasattr(request.user, 'workerprofile'):
        template_name = 'usuarios/home_trabajador.html'
        
        # Obtenemos el perfil (manejando ambos nombres de relación por si acaso)
        perfil = getattr(request.user, 'worker_profile', None) or getattr(request.user, 'workerprofile', None)
        
        if perfil:
            # Filtramos las solicitudes del trabajador
            solicitudes_todas = JobRequest.objects.filter(worker=perfil)
            
            # Pasamos datos al contexto
            context['solicitudes_recientes'] = solicitudes_todas.order_by('-created_at')[:3]
            context['total_completados'] = solicitudes_todas.filter(status='COMPLETED').count()
            context['nuevas_solicitudes'] = solicitudes_todas.filter(status='PENDING').count()
            
            # Si tienes un método para el promedio en tu modelo WorkerProfile, úsalo aquí
            context['promedio'] = getattr(perfil, 'get_average_rating', 0.0)
    
    # 3. Caso: Usuario sin perfil o Admin
    else:
        template_name = 'usuarios/home.html'

    response = render(request, template_name, context)
    
    # Cabeceras de limpieza de caché
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    return response

@login_required
def completar_perfil_cliente(request):
    perfil, created = ClientProfile.objects.get_or_create(user=request.user)
    if created:
        titulo_pantalla = "¡Bienvenido! Crea tu perfil de cliente"
        subtitulo = "Por favor, completa tus datos para empezar a solicitar servicios."
    else:
        titulo_pantalla = "Editar Perfil"
        subtitulo = "Actualiza tu información personal a continuación."
    if request.method == 'POST':
        form = ClientProfileForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ClientProfileForm(instance=perfil)
    context = {
        'form': form,
        'perfil': perfil,
        'titulo': titulo_pantalla,
        'subtitulo': subtitulo,
        'nuevo_perfil': created 
    }

    return render(request, 'usuarios/completar_perfil_cliente.html', context)

@login_required
def completar_perfil_trabajador(request):
    # 1. Obtener o crear el perfil
    perfil, created = WorkerProfile.objects.get_or_create(user=request.user)
    
    # 2. Lógica de 'created': Definir un mensaje según el estado
    if created:
        titulo_pantalla = "¡Bienvenido! Crea tu perfil de trabajador"
        subtitulo = "Por favor, completa tus datos para empezar a ofrecer tus servicios."
    else:
        titulo_pantalla = "Editar Perfil"
        subtitulo = "Actualiza tu información profesional a continuación."

    # 3. Procesamiento del Formulario   
    if request.method == 'POST':
        form = WorkerProfileForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = WorkerProfileForm(instance=perfil)
    
    context = {
        'form': form, 
        'titulo_pantalla': titulo_pantalla,
        'subtitulo': subtitulo
        }
    return render(request,'usuarios/completar_perfil_trabajador.html', context)

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        tipo_usuario = request.POST.get('tipo_usuario') 

        if password1 != password2:
            return render(request, 'usuarios/register.html', {'error': 'Las contraseñas no coinciden'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'usuarios/register.html', {'error': '¡El usuario ya existe!'})
        
        user = User.objects.create_user(username=username, password=password1)
        login(request, user)
        
        if tipo_usuario == 'trabajador':
            WorkerProfile.objects.get_or_create(user=user)
            # SOLUCIÓN: Usamos la ruta absoluta exacta que definiste en tu urls.py
            return redirect('/perfil/completar/')          
        
        elif tipo_usuario == 'cliente':
            ClientProfile.objects.get_or_create(user=user)
            # CORRECCIÓN DE BUG: Redirigimos a la ruta absoluta del cliente
            return redirect('/completar_perfil/')
            
    return render(request, 'usuarios/register.html')

