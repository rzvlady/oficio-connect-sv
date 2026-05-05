from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
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
            return render(request, 'servicios/perfil_trabajador.html', {
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
                return redirect('perfil_trabajador', worker_id=trabajador.id)
            except ValidationError:
                form.add_error(None, "Ya has calificado a este trabajador anteriormente.")
            else:
                pass
    return render(request, 'servicios/perfil_trabajador.html', {
        'worker': trabajador,
        'form': form,
        'existe_trabajo': tiene_trabajo 
    })

#category 

def lista_categorias(request):
    categorias = Category.objects.all()
    return render(request, "lista_categorias.html", {"categorias":categorias})

def crear_categoria(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("lista_categorias")
    return render(request, "crear_categoria.html",{"form":form})

def editar_categoria(request,id):
    categoria = Category.objects.get(id=id)
    form = CategoryForm(request.POST or None, instance=categoria)
    if form.is_valid():
        form.save()
        return redirect("lista_categorias")
    return render(request, "editar_categorias.html",{"form":form})

def eliminar_categoria(request, id):
    categoria = Category.objects.get(id=id)
    categoria.delete()
    return redirect("lista_categorias")

#trabajadores
def lista_workers(request):
    workers = WorkerProfile.objects.all()
    return render(request, "servicios/perfil_trabajador.html", {"workers":workers})

def crear_worker(request):
    form = WorkerProfileForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("lista_workers")
    return render(request, "servicios/crear_worker.html",{"form":form})

def editar_worker(request,id):
    worker = WorkerProfile.objects.get(id=id)
    form = WorkerProfileForm(request.POST or None, instance=worker)
    if form.is_valid():
        form.save()
        return redirect("lista_workers")
    return render(request, "servicios/editar_worker.html",{"form":form})

def eliminar_worker(request, id):
    worker = WorkerProfile.objects.get(id=id)
    worker.delete()
    return redirect("lista_workers")

def login_view(request):
    return render(request, 'usuarios/login.html')

def register_view(request):
    return render(request, 'usuarios/register.html')