from django.urls import path
from . import views

urlpatterns = [
    path('review_trabajador/<int:worker_id>/', views.crear_resena, name='review_trabajador'),

    path('explorar/', views.lista_categorias_cliente, name='explorar_categorias'),

    path('explorar/<int:categoria_id>/', views.trabajadores_por_categoria, name='trabajadores_categoria'),

    path('trabajador/<int:trabajador_id>/', views.detalle_trabajador, name='detalle_trabajador'),

    path('solicitar/<int:worker_id>/', views.solicitar_trabajo, name='solicitar_trabajo'),
    
    path('mis-solicitudes/', views.mis_solicitudes, name='mis_solicitudes'),

    path('solicitud/<int:request_id>/chat/', views.chat_solicitud, name='chat_solicitud'),

    path('solicitud/<int:solicitud_id>/cambiar-estado/', views.cambiar_estado_solicitud, name='cambiar_estado_solicitud'),

]

