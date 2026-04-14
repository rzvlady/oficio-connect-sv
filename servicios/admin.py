from django.contrib import admin
<<<<<<< Updated upstream

# Register your models here.
=======
from .models import WorkerProfile, Review, Category

admin.site.register(WorkerProfile)
admin.site.register(Review)
admin.site.register(Category)

>>>>>>> Stashed changes
