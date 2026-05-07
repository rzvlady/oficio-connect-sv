from django import forms
from .models import Review, Category, WorkerProfile

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Cuéntanos tu experiencia...',
                'rows': 3
            }),
        }   

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class WorkerProfileForm(forms.ModelForm):
    class Meta:
        model = WorkerProfile
        fields = '__all__'
