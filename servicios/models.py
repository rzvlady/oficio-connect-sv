from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.core.exceptions import ValidationError

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class WorkerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="workers")
    bio = models.TextField(help_text="Breve descripción de su experiencia en el trabajo")
    phone_number = models.CharField(max_length=15)
    service_area = models.CharField(max_length=100, default="San Salvador")
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def total_reviews(self):
        return self.reviews.count()

    def get_average_rating(self):
        result = self.reviews.aggregate(Avg('rating', default = 0))['rating__avg']
        return round(result, 2)  
    #retorna el resultado redondeado dos decimales
        """el uso de "__" es parte de la convencion de nombres de django, se hace para no confundir con variables propias
        si estuviera sumando usaria algo__sum. aggregate retorna un diccionaro, por eso se usa  ['rating__avg']
        Es como si el nombre se asignara sobre la marcha. ['rating__avg'] es la key y lo que round(result, 1) el value"""

    def get_stars_number(self):
        rating = self.get_average_rating()
        full_stars = int(rating)
        stars_decimal_part = rating - full_stars
        half_star = 0

        if stars_decimal_part >= 0.75:
            full_stars +=1

        elif stars_decimal_part >= 0.25:
            half_star = 1

        elif stars_decimal_part < 0.25:
            half_star = 0
        empty_stars = 5 - (full_stars + half_star)

        return {
            'full_stars': range(full_stars),
            'half_stars': range(half_star),
            'empty_stars': range(empty_stars)
        }
        """esta funcion permie que ne el front se puedan mostrar graficamente
          calificaciones como '3 estrellas y la mitad de una' o sea, (3.5 estrellas o )"""

    def __str__(self):
        return f"{self.full_name} - {self.category.name}"
    
class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client_profile")
    full_name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255, help_text="Dirección para recibir el servicio")
    municipality = models.CharField(max_length=100, default="San Salvador", verbose_name="Municipio") #quitar eso total es solo en el AMSS
    profile_picture = models.ImageField(upload_to='clients/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cliente: {self.full_name}"
    
class Review(models.Model):
    worker = models.ForeignKey(WorkerProfile, on_delete=models.CASCADE, related_name="reviews")
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.worker.user == self.client.user:  
            raise ValidationError("No puede calificarse a sí mismo")
        
        has_completed_job = JobRequest.objects.filter(
            client=self.client, 
            worker=self.worker, 
            status='COMPLETED'
        ).exists()
        if not has_completed_job:
            raise ValidationError("Debes completar un trabajo con este profesional antes de calificarlo.")
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ("worker", "client")

    def __str__(self):
        return f"Review de {self.worker.full_name} por {self.client.full_name}"

class JobRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('ACCEPTED', 'Aceptado'),
        ('COMPLETED', 'Completado'),
        ('CANCELLED', 'Cancelado'),
    ]
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    worker = models.ForeignKey(WorkerProfile, on_delete=models.CASCADE)
    description = models.TextField(help_text="¿Qué necesita que el trabajador haga?")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Servicio de {self.worker.full_name} para {self.client.full_name}"
    
 # nombre_columna = models.TipoDeDato(configuraciones, validaciones, relaciones)