from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('home/', views.home_view, name='home'),

    path('register/', views.register_view, name='register'),

    path('completar_perfil/', views.completar_perfil_cliente, name='completar_perfil_cliente'),

    path('review_trabajador/<int:worker_id>/', views.crear_resena, name='review_trabajador'), 

    path('explorar/', views.lista_categorias_cliente, name='explorar_categorias'),

    path('explorar/<int:categoria_id>/', views.trabajadores_por_categoria, name='trabajadores_categoria'),

    path('perfil/completar/', views.completar_perfil_trabajador, name='completar_perfil_trabajador'),

    #path('categorias/', views.lista_categorias, name='lista_categorias'),

    #path('categorias/crear/', views.crear_categoria, name = 'crear_categoria'), 

    #path('categorias/editar/<int:id>/', views.editar_categoria, name = 'editar_categoria'),

    #path('categorias/eliminar/<int:id>', views.eliminar_categoria, name = 'eliminar_categoria'),

    path('workers/', views.lista_workers, name='lista_workers'),

    #path('workers/crear/', views.crear_worker, name = 'crear_worker'), 

    path('workers/editar/<int:id>/', views.editar_worker, name = 'editar_worker'),

    path('workers/eliminar/<int:id>', views.eliminar_worker, name = 'eliminar_worker'), 

]