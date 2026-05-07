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
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        tipo_usuario = request.POST.get('tipo_usuario') # Capturamos qué eligió

        if password1 != password2:
            return render(request, 'usuarios/register.html', {'error': 'Las contraseñas no coinciden'})
            
        if User.objects.filter(username=username).exists():
            return render(request, 'usuarios/register.html', {'error': '¡El usuario ya existe!'})
            
        # 1. Creamos el usuario base
        user = User.objects.create_user(username=username, password=password1)
        
        # 2. Creamos el perfil correspondiente en blanco
        if tipo_usuario == 'trabajador':
            WorkerProfile.objects.create(user=user, full_name=username)
        elif tipo_usuario == 'cliente':
            ClientProfile.objects.create(user=user, full_name=username)
            
        # 3. Iniciamos sesión y redirigimos
        login(request, user)
        return redirect('home')
        
    return render(request, 'usuarios/register.html')