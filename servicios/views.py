from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, PermissionDenied
from .models import Category, WorkerProfile, ClientProfile, Review, JobRequest
from .forms import ReviewForm, CategoryForm, WorkerProfileForm
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

def lista_categorias(request):
    categorias = Category.objects.all()
    return render(request, "servicios/lista_categorias.html", {"categorias":categorias})

def crear_categoria(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("lista_categorias")
    return render(request, "servicios/crear_categoria.html",{"form":form})

def editar_categoria(request,id):
    categoria = Category.objects.get(id=id)
    form = CategoryForm(request.POST or None, instance=categoria)
    if form.is_valid():
        form.save()
        return redirect("lista_categorias")
    return render(request, "servicios/editar_categorias.html",{"form":form})

def eliminar_categoria(request, id):
    categoria = Category.objects.get(id=id)
    categoria.delete()
    return redirect("lista_categorias")

#trabajadores
def lista_workers(request):
    workers = WorkerProfile.objects.all()
    return render(request, "servicios/lista_workers.html", {"workers":workers})

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
    return render(request,'servicios/completar_perfil_trabajador.html', context)

@login_required
def crear_worker(request):
    form = WorkerProfileForm(request.POST or None)
    if form.is_valid():
        worker = form.save(commit=False)
        worker.user = request.user
        worker.save()
        return redirect("lista_workers")
    return render(request, "servicios/crear_worker.html",{"form":form})

@login_required
def editar_worker(request,id):
    worker = get_object_or_404(WorkerProfile, id=id, user=request.user)
    form = WorkerProfileForm(request.POST or None, instance=worker)
    if form.is_valid():
        form.save()
        return redirect("lista_workers")
    return render(request, "servicios/editar_worker.html",{"form":form})

@login_required
def eliminar_worker(request, id):
    worker = get_object_or_404(worker, id=id, user=request.user)
    worker.delete()
    return redirect("lista_workers")



