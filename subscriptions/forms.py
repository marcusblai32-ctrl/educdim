from django import forms
from django.utils.translation import gettext as _
from .models import Subscription, SubscriptionCourseSelection


class SubscriptionForm(forms.ModelForm):
    """Fòmilè pou kreye yon abònman (DEJA EGZISTE - PA TOUCHE)."""
    
    class Meta:
        model = Subscription
        fields = ['methode_paiement', 'nom_compte', 'telephone', 'id_transaction', 'photo_paiement']
        widgets = {
            'methode_paiement': forms.Select(attrs={'class': 'form-control'}),
            'nom_compte': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du compte'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numéro de téléphone'}),
            'id_transaction': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID de transaction'}),
            'photo_paiement': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super().clean()
        methode = cleaned_data.get('methode_paiement')
        
        if methode == 'moncash':
            if not cleaned_data.get('id_transaction'):
                self.add_error('id_transaction', _("L'ID de transaction est requis pour MonCash."))
            if not cleaned_data.get('telephone'):
                self.add_error('telephone', _("Le numéro de téléphone est requis pour MonCash."))
        elif methode == 'natcash':
            if not cleaned_data.get('photo_paiement'):
                self.add_error('photo_paiement', _("La photo de paiement est requise pour NatCash."))
        
        return cleaned_data


class CourseSelectionForm(forms.Form):
    """NOUVO FÒMILÈ: Pou chwazi kou yo."""
    
    courses = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Choisissez vos cours"
    )
    
    def __init__(self, *args, **kwargs):
        subscription = kwargs.pop('subscription', None)
        super().__init__(*args, **kwargs)
        
        if subscription:
            # Filtrer kou ki disponib yo
            self.fields['courses'].queryset = subscription.get_courses_disponibles()
            
            # Ajoute max limit kòm atribi pou JavaScript
            if subscription.plan.max_courses > 0:
                self.fields['courses'].widget.attrs.update({
                    'data-max-courses': subscription.plan.max_courses,
                    'data-subscription-id': subscription.pk,
                })
    
    def clean_courses(self):
        courses = self.cleaned_data.get('courses')
        if courses and courses.count() == 0:
            raise forms.ValidationError(_("Veuillez sélectionner au moins un cours."))
        return courses