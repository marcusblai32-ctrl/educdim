from .models import Banner

def banners_processor(request):
    headers = Banner.objects.filter(actif=True, placement='header').order_by('ordre')
    sidebars = Banner.objects.filter(actif=True, placement='sidebar').order_by('ordre')
    footers = Banner.objects.filter(actif=True, placement='footer').order_by('ordre')
    return {
        'banners_header': headers,
        'banners_sidebar': sidebars,
        'banners_footer': footers,
    }
