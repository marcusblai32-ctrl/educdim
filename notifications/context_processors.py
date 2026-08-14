from .models import Notification

def unread_notifications_count(request):
    count = 0
    if request.user.is_authenticated:
        count = Notification.objects.filter(utilisateur=request.user, lue=False).count()
    return {'unread_notifications': count}
