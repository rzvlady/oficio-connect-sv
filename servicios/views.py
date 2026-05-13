from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .models import Category, WorkerProfile, ClientProfile, JobRequest, Message
from .forms import ReviewForm, JobRequestForm, MessageForm
from django.contrib import messages

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

@login_required(login_url='login')
def solicitar_trabajo(request, worker_id):
    try:
        cliente = request.user.client_profile
    except ObjectDoesNotExist:
        messages.error(request, "Tu cuenta no tiene un perfil de cliente registrado.")
        return redirect('home')

    trabajador = get_object_or_404(WorkerProfile, id=worker_id)

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
    es_cliente = hasattr(request.user, 'client_profile')
    es_trabajador = hasattr(request.user, 'worker_profile')

    if es_cliente:
        solicitudes = JobRequest.objects.filter(client=request.user.client_profile).order_by('-created_at')
        rol = 'cliente'
    elif es_trabajador:
        solicitudes = JobRequest.objects.filter(worker=request.user.worker_profile).order_by('-created_at')
        rol = 'trabajador'
    else:
        messages.error(request, "Acceso denegado. No tienes un perfil válido.")
        return redirect('home')

    return render(request, 'servicios/mis_solicitudes.html', {
        'solicitudes': solicitudes,
        'rol': rol
    })
    
@login_required(login_url='login')
def chat_solicitud(request, request_id):
    job_request = get_object_or_404(JobRequest, id=request_id)

    es_cliente = hasattr(request.user, 'client_profile') and job_request.client == request.user.client_profile
    es_trabajador = hasattr(request.user, 'worker_profile') and job_request.worker == request.user.worker_profile

    if not (es_cliente or es_trabajador):
        messages.error(request, "No tienes permiso para ver esta conversación.")
        return redirect('home')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.job_request = job_request
            mensaje.sender = request.user
            
            if es_cliente:
                mensaje.receiver = job_request.worker.user
            else:
                mensaje.receiver = job_request.client.user
                
            mensaje.save() 
            return redirect('chat_solicitud', request_id=job_request.id)
    else:
        form = MessageForm()
    mensajes = job_request.mensajes.all()
    context = {
        'job_request': job_request,
        'mensajes': mensajes,
        'form': form,  
    }
    return render(request, 'servicios/chat_solicitud.html', context)    

@login_required(login_url='login')
def cambiar_estado_solicitud(request, solicitud_id):
    if request.method == 'POST':
        solicitud = get_object_or_404(JobRequest, id=solicitud_id)
        es_cliente = hasattr(request.user, 'client_profile') and solicitud.client == request.user.client_profile
        es_trabajador = hasattr(request.user, 'worker_profile') and solicitud.worker == request.user.worker_profile

        if not (es_cliente or es_trabajador):
            return redirect('home')

        accion = request.POST.get('accion')
        if accion == 'ACEPTAR' and es_trabajador and solicitud.status == 'PENDING':
            solicitud.status = 'ACCEPTED'
            solicitud.save()
            messages.success(request, "Has aceptado el trabajo.")

        elif accion in ['COMPLETAR', 'CANCELAR'] and solicitud.status == 'ACCEPTED':
            voto = 'COMPLETED' if accion == 'COMPLETAR' else 'CANCELLED'
            if es_cliente:
                solicitud.client_confirmation = voto
            else:
                solicitud.worker_confirmation = voto
            solicitud.save()
            if solicitud.client_confirmation and solicitud.worker_confirmation:
                if solicitud.client_confirmation == solicitud.worker_confirmation:
                    solicitud.status = solicitud.client_confirmation
                    solicitud.save()
                    messages.success(request, f"¡El trabajo ha sido marcado como {solicitud.get_status_display()} por ambos!")
                else:
                    messages.warning(request, "Hay un desacuerdo. Uno marcó completado y el otro cancelado. Por favor, discútanlo en el chat.")
            else:
                messages.info(request, "Has registrado tu confirmación. Esperando a que la otra parte confirme.")

    return redirect('mis_solicitudes')

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
