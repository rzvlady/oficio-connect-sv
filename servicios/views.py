from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import Category, WorkerProfile, ClientProfile, Review, JobRequest
from .forms import ReviewForm
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


