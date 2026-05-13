from servicios.models import ClientProfile, WorkerProfile
from django import forms


class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ['full_name', 'phone_number', 'address', 'municipality', 'profile_picture']
        
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 7777-7777'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Colonia, calle, # de casa'}),
            'municipality': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

class WorkerProfileForm(forms.ModelForm):
    class Meta:
        model = WorkerProfile
        exclude = ['user'] 

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 7777-7777'}),
            'service_area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. San Salvador...'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Escribe aquí tu experiencia...'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }