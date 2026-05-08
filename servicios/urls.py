from django.urls import path, include
from . import views

urlpatterns = [
    path('review_trabajador/<int:worker_id>/', views.crear_resena, name='review_trabajador'), 

    path('explorar/', views.lista_categorias_cliente, name='explorar_categorias'),

    path('explorar/<int:categoria_id>/', views.trabajadores_por_categoria, name='trabajadores_categoria'),


    #path('categorias/', views.lista_categorias, name='lista_categorias'),

    #path('categorias/crear/', views.crear_categoria, name = 'crear_categoria'), 

    #path('categorias/editar/<int:id>/', views.editar_categoria, name = 'editar_categoria'),

    #path('categorias/eliminar/<int:id>', views.eliminar_categoria, name = 'eliminar_categoria'),

    #path('workers/', views.lista_workers, name='lista_workers'),

    #path('workers/crear/', views.crear_worker, name = 'crear_worker'), 

    #path('workers/editar/<int:id>/', views.editar_worker, name = 'editar_worker'),

    #path('workers/eliminar/<int:id>', views.eliminar_worker, name = 'eliminar_worker'), 

]

