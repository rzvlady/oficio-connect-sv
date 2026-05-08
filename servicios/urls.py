from django.urls import path
from . import views

urlpatterns = [
    path('review_trabajador/<int:worker_id>/', views.crear_resena, name='review_trabajador'),

    path('explorar/', views.lista_categorias_cliente, name='explorar_categorias'),

    path('explorar/<int:categoria_id>/', views.trabajadores_por_categoria, name='trabajadores_categoria'),

    path('trabajador/<int:trabajador_id>/', views.detalle_trabajador, name='detalle_trabajador'),

    path('perfil/completar/', views.completar_perfil_trabajador, name='completar_perfil_trabajador'),

    path('workers/', views.lista_workers, name='lista_workers'),

    path('workers/editar/<int:id>/', views.editar_worker, name='editar_worker'),

    path('workers/eliminar/<int:id>/', views.eliminar_worker, name='eliminar_worker'),
    
]

