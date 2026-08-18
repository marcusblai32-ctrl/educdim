from .models import Theme
from django.utils.translation import gettext as _

def theme_processor(request):
    """Ajoute tema aktif la nan tout paj yo"""
    theme = Theme.objects.filter(actif=True).first()
    if not theme:
        # Kreye yon tema pa defo si pa genyen
        theme = Theme.objects.create(actif=True)
    return {
        'theme': theme,
        'maintenance_mode': theme.maintenance_mode if theme else False,
        'maintenance_message': theme.maintenance_message if theme else "",
    }

def breadcrumbs_processor(request):
    """Kreye breadcrumbs pou navigasyon an"""
    path = request.path
    parts = path.strip('/').split('/')
    breadcrumbs = []
    current_path = ''

    # Sote prefiks lang (fr/, ht/)
    start_idx = 0
    if parts and parts[0] in ['fr', 'ht']:
        start_idx = 1

    # Map non URL yo
    names = {
        # Apps prensipal
        'cours': _('Cours'),
        'inscriptions': _('Inscriptions'),
        'progression': _('Progression'),
        'quiz': _('Quiz'),
        'presence': _('Présences'),
        'badges': _('Badges'),
        'classement': _('Classement'),
        'chat': _('Chat'),
        'notifications': _('Notifications'),
        'contact': _('Contact'),
        'a-propos': _('À propos'),
        'conditions': _('Conditions'),
        'confidentialite': _('Confidentialité'),
        'faq': _('FAQ'),
        'dashboard': _('Tableau de bord'),
        'todo': _('Todo'),
        'theme': _('Thème'),
        'ads': _('Annonces'),
        # Akò
        'connexion': _('Connexion'),
        'inscription': _('Inscription'),
        'profil': _('Profil'),
        'supprimer': _('Supprimer'),
        'mot-de-passe-oublie': _('Mot de passe oublié'),
        'reinitialiser': _('Réinitialiser'),
        'modifier': _('Modifier'),
        'ajouter': _('Ajouter'),
        'liste': _('Liste'),
        'detail': _('Détail'),
    }

    for part in parts[start_idx:]:
        if part:
            current_path += '/' + part
            # Sèvi ak non ki nan diksyonè a oswa mete majiskil
            name = names.get(part, part.replace('-', ' ').replace('_', ' ').title())
            breadcrumbs.append({'name': name, 'url': current_path})

    return {'breadcrumbs': breadcrumbs}

def seo_processor(request):
    """Ajoute meta description ak meta keywords pou SEO"""
    theme = Theme.objects.filter(actif=True).first()
    return {
        'meta_description': theme.meta_description if theme else '',
        'meta_keywords': theme.meta_keywords if theme else '',
    }
