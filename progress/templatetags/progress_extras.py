from django import template

register = template.Library()

@register.filter
def length_custom(value):
    """Retounen kantite lekon ki fini"""
    if not value:
        return 0
    count = 0
    for item in value:
        if item.get('progres') and item['progres'].statut == 'termine':
            count += 1
    return count