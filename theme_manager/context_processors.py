from .models import Theme
from django.utils.translation import gettext as _

def theme_processor(request):
    theme = Theme.objects.filter(actif=True).first()
    if not theme:
        theme = Theme.objects.create(actif=True)
    return {
        'theme': theme,
        'maintenance_mode': theme.maintenance_mode if theme else False,
        'maintenance_message': theme.maintenance_message if theme else "",
    }

def breadcrumbs_processor(request):
    path = request.path
    parts = path.strip('/').split('/')
    breadcrumbs = []
    current_path = ''

    start_idx = 0
    if parts and parts[0] in ['fr', 'ht']:
        start_idx = 1

    for part in parts[start_idx:]:
        if part:
            current_path += '/' + part
            names = {
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
            }
            name = names.get(part, part.replace('-', ' ').replace('_', ' ').title())
            breadcrumbs.append({'name': name, 'url': current_path})

    return {'breadcrumbs': breadcrumbs}

def seo_processor(request):
    theme = Theme.objects.filter(actif=True).first()
    return {
        'meta_description': theme.meta_description if theme else '',
        'meta_keywords': theme.meta_keywords if theme else '',
    }
