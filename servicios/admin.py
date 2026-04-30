from django.contrib import admin
from .models import WorkerProfile, Review, Category, JobRequest, ClientProfile

admin.site.register(WorkerProfile)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(JobRequest)
admin.site.register(ClientProfile)


# Register your models here.
