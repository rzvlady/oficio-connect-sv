from django import forms
from .models import Review, Category, WorkerProfile, ClientProfile

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

from django import forms
from .models import JobRequest

class JobRequestForm(forms.ModelForm):
    class Meta:
        model = JobRequest
        fields = ['description', 'address_reference', 'evidencia_foto']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Ej. El chorro de la cocina tiene una fuga...'}),
            'address_reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Casa de portón negro frente al parque'}),
            'evidencia_foto': forms.FileInput(attrs={'class': 'form-control'}),
        }

