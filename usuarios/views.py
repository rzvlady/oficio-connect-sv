from .forms import ClientProfileForm
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

@login_required(login_url='login')
def home_view(request):
    # Intentamos detectar el perfil del cliente
    if hasattr(request.user, 'client_profile'):
        template_name = 'usuarios/home_cliente.html'
    
    # Intentamos detectar el perfil del trabajador 
    # (Ojo: si no pusiste related_name, Django usa 'workerprofile')
    elif hasattr(request.user, 'worker_profile') or hasattr(request.user, 'workerprofile'):
        template_name = 'usuarios/home_trabajador.html'
    
    else:
        # Si es un admin o usuario nuevo sin perfil
        template_name = 'usuarios/home.html'

    response = render(request, template_name)
    
    # Tus cabeceras de limpieza de caché
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    return response

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
            return redirect('completar_perfil_trabajador')           
        elif tipo_usuario == 'cliente':
            ClientProfile.objects.get_or_create(user=user)
            return redirect('completar_perfil_cliente')
            
    return render(request, 'usuarios/register.html')

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