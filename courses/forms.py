from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'titre', 'description', 'image_url', 'image',
            'prix', 'publie', 'categorie', 'nivo',
            'duree', 'date_debut_inscription', 'date_fin_inscription',
            'inscription_ouverte'
        ]
        widgets = {
            'date_debut_inscription': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'date_fin_inscription': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'duree': forms.NumberInput(attrs={'min': 0}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }
