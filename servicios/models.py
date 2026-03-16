from django.db import models
from django.contrib.auth.models import User

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

    def __str__(self):
        return f"{self.full_name} - {self.category.name}"
    
class Review(models.Model):
    worker = models.ForeignKey(WorkerProfile, on_delete=models.CASCADE, related_name="reviews")
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("worker", "client")

    def __str__(self):
        return f"Review de {self.worker.full_name} por {self.client.username}"