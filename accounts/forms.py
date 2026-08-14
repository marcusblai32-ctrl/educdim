from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'birth_year', 'password1', 'password2')
        labels = {
            'email': 'Email',
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'birth_year': 'Année de naissance',
        }
        widgets = {
            'birth_year': forms.NumberInput(attrs={'min': 1900, 'max': 2026}),
        }

    def clean_birth_year(self):
        year = self.cleaned_data.get('birth_year')
        import datetime
        current_year = datetime.datetime.now().year
        if year < 1900 or year > current_year:
            raise forms.ValidationError("Année de naissance invalide.")
        return year
