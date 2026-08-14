from django import forms
from .models import Subscription

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['methode_paiement', 'nom_compte', 'telephone', 'id_transaction', 'photo_paiement']
        widgets = {
            'nom_compte': forms.TextInput(attrs={'placeholder': 'Ex: Jean Dupont'}),
            'telephone': forms.TextInput(attrs={'placeholder': '509XXXXXXXX'}),
            'id_transaction': forms.TextInput(attrs={'placeholder': 'ID de la transaction'}),
            'photo_paiement': forms.FileInput(attrs={'accept': 'image/*'}),
        }
        labels = {
            'methode_paiement': 'Méthode de paiement',
            'nom_compte': 'Nom sur le compte',
            'telephone': 'Numéro de téléphone',
            'id_transaction': 'ID de transaction',
            'photo_paiement': 'Photo du paiement',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user and self.user.is_staff:
            self.fields['methode_paiement'].choices = [
                ('moncash', 'MonCash'),
                ('natcash', 'NatCash'),
                ('manual', 'Attribution manuelle (admin)'),
            ]
        else:
            self.fields['methode_paiement'].choices = [
                ('moncash', 'MonCash'),
                ('natcash', 'NatCash'),
            ]
