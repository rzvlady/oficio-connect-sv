from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .models import Category, WorkerProfile, ClientProfile, JobRequest
from .forms import ReviewForm, JobRequestForm
from django.contrib import messages

@login_required
def crear_resena(request, worker_id):
    trabajador = get_object_or_404(WorkerProfile, id=worker_id)

    cliente = get_object_or_404(ClientProfile, user=request.user)

    tiene_trabajo = JobRequest.objects.filter(
        worker = trabajador,
        client = cliente,
        status = 'COMPLETED'
    ).exists()

    form = ReviewForm(request.POST or None)

    if request.method == 'POST':
        if not tiene_trabajo:
            return render(request, 'servicios/review_trabajador.html', {
                'worker': trabajador,
                'error_mensaje': "No puedes calificar sin un trabajo completado.",
                'form': form,
                })
        form.instance.worker = trabajador
        form.instance.client = cliente

        if form.is_valid():
            try:
                form.save() 
                messages.success(request, "¡Gracias! Tu reseña ha sido publicada con éxito.")
                return redirect('review_trabajador', worker_id=trabajador.id)
            except ValidationError:
                form.add_error(None, "Ya has calificado a este trabajador anteriormente.")
            else:
                pass
    return render(request, 'servicios/review_trabajador.html', {
        'worker': trabajador,
        'form': form,
        'existe_trabajo': tiene_trabajo 
    })

def lista_categorias_cliente(request):
    categorias = Category.objects.all()
    return render(request, 'servicios/cliente_categorias.html', {'categorias': categorias})

def trabajadores_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Category, id=categoria_id)
    trabajadores = WorkerProfile.objects.filter(category=categoria)
    
    return render(request, 'servicios/cliente_trabajadores.html', {
        'categoria': categoria,
        'trabajadores': trabajadores
    })

@login_required(login_url='login')
def detalle_trabajador(request, trabajador_id):
    trabajador = get_object_or_404(WorkerProfile.objects.select_related('user'), id=trabajador_id)
    resenas = trabajador.reviews.select_related('client__user').all().order_by('-id') 
    context = {
        'trabajador': trabajador,
        'resenas': resenas,
    }
    return render(request, 'servicios/detalle_trabajador.html', context)


# Asegúrate de tener tus otras importaciones aquí (messages, redirect, render, etc.)

@login_required(login_url='login')
def solicitar_trabajo(request, worker_id):
    
    # 1. Validar que el usuario sea un Cliente y obtener su perfil
    try:
        cliente = request.user.client_profile
    except ObjectDoesNotExist:
        messages.error(request, "Tu cuenta no tiene un perfil de cliente registrado.")
        return redirect('home')

    # 2. Obtener el perfil del trabajador al que se le pide el servicio
    trabajador = get_object_or_404(WorkerProfile, id=worker_id)

    # 3. Procesar el formulario
    if request.method == 'POST':
        form = JobRequestForm(request.POST, request.FILES)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.client = cliente  
            solicitud.worker = trabajador
            solicitud.save()
            
            messages.success(request, f"¡Tu solicitud a {trabajador.user.username} ha sido enviada con éxito!")
            return redirect('mis_solicitudes')
    else:
        form = JobRequestForm()

    context = {
        'form': form,
        'trabajador': trabajador
    }
    return render(request, 'servicios/solicitar_trabajo.html', context)

@login_required(login_url='login')
def mis_solicitudes(request):
    try:
        cliente = request.user.client_profile
    except ObjectDoesNotExist:
        messages.error(request, "Acceso denegado. No tienes un perfil de cliente.")
        return redirect('home')
    solicitudes = JobRequest.objects.filter(client=cliente).order_by('-created_at')

    return render(request, 'servicios/mis_solicitudes.html', {
        'solicitudes': solicitudes
    })
    
