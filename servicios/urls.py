from django.urls import path
from . import views

urlpatterns = [
    path('trabajador/<int:worker_id>/', views.crear_resena, name='perfil_trabajador'),
]