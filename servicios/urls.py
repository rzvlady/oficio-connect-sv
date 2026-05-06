from django.urls import path
from . import views

urlpatterns = [
    path('review_trabajador/<int:worker_id>/', views.crear_resena, name='review_trabajador'),
]