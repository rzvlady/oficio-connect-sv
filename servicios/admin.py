from django.contrib import admin
from .models import WorkerProfile, Review, Category


admin.site.register(WorkerProfile)
admin.site.register(Review)
admin.site.register(Category)















from .models import Category, WorkerProfile, Review

admin.site.register(Category)
admin.site.register(WorkerProfile)
admin.site.register(Review)
