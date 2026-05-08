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
    response = render(request, 'usuarios/home.html')
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
            
        # 1. Creamos el usuario base
        user = User.objects.create_user(username=username, password=password1)
        
        # 2. Iniciamos sesión de una vez
        login(request, user)
        
        # 3. Redirección y creación según el tipo
        if tipo_usuario == 'trabajador':
            WorkerProfile.objects.get_or_create(user=user)
            # Cambiamos 'home' por la vista de perfil de trabajador (cuando la tengas)
            return redirect('completar_perfil_trabajador') 
            
        elif tipo_usuario == 'cliente':
            ClientProfile.objects.get_or_create(user=user)
            # Aquí es donde lo mandamos a la vista que acabamos de hacer
            return redirect('completar_perfil_cliente')
            
    return render(request, 'usuarios/register.html')

@login_required
def completar_perfil_cliente(request):
    # 1. Obtener o crear el perfil
    perfil, created = ClientProfile.objects.get_or_create(user=request.user)
    
    # 2. Lógica de 'created': Definir un mensaje según el estado
    if created:
        titulo_pantalla = "¡Bienvenido! Crea tu perfil de cliente"
        subtitulo = "Por favor, completa tus datos para empezar a solicitar servicios."
    else:
        titulo_pantalla = "Editar Perfil"
        subtitulo = "Actualiza tu información personal a continuación."

    # 3. Procesamiento del Formulario   
    if request.method == 'POST':
        form = ClientProfileForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ClientProfileForm(instance=perfil)

    # 4. Pasar las variables al HTML
    context = {
        'form': form,
        'perfil': perfil,
        'titulo': titulo_pantalla,
        'subtitulo': subtitulo,
        'nuevo_perfil': created # También puedes pasar el booleano directamente
    }

    return render(request, 'usuarios/completar_perfil.html', context)