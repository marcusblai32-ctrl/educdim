from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone

class UpdateActivityMiddleware(MiddlewareMixin):
    """Met ajou aktivite itilizatè a chak fwa yon reqèt fèt"""

    def process_request(self, request):
        if request.user.is_authenticated:
            if hasattr(request.user, 'last_activity'):
                delta = timezone.now() - request.user.last_activity
                if delta.seconds > 600:  # 10 minit
                    request.user.last_activity = timezone.now()
                    request.user.save(update_fields=['last_activity'])
