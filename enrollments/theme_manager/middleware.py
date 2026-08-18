import logging
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
from .models import Theme
from django.db import DatabaseError, OperationalError, ProgrammingError

logger = logging.getLogger(__name__)

class MaintenanceMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            if request.path.startswith('/dp/') or request.path.startswith('/static/') or request.path.startswith('/media/'):
                return None

            try:
                if request.user.is_authenticated and request.user.is_staff:
                    return None
            except Exception:
                logger.exception("Error checking user staff status")

            try:
                theme = Theme.objects.filter(actif=True).first()
            except (ProgrammingError, OperationalError, DatabaseError):
                return None

            if not theme or not theme.maintenance_mode:
                return None

            return render(request, 'maintenance.html', {
                'message': theme.maintenance_message,
                'theme': theme,
            })
        except Exception:
            logger.exception("Unhandled exception in MaintenanceMiddleware")
            return None
