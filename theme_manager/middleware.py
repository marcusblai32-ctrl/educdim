from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
from .models import Theme

class MaintenanceMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Pa bloke admin, static, media
        if request.path.startswith('/dp/') or request.path.startswith('/static/') or request.path.startswith('/media/'):
            return None

        # Pa bloke si user se staff oswa superuser (tout staff)
        if request.user.is_authenticated and request.user.is_staff:
            return None

        # Pa bloke si maintenance pa aktif
        theme = Theme.objects.filter(actif=True).first()
        if not theme or not theme.maintenance_mode:
            return None

        # Bloke tout lòt moun
        return render(request, 'maintenance.html', {
            'message': theme.maintenance_message,
            'theme': theme,
        })
